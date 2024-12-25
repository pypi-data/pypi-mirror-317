"""Backend server for Gallagher plugins."""

from __future__ import annotations

import argparse
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
import os
import shutil
from typing import Any

from fastapi import FastAPI, File, HTTPException, Request, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import FileResponse
import uvicorn

from pconn.helpers.file_upload import (
    DOMAIN as FILE_UPLOAD_DOMAIN,
    FileUploadData,
    FileUploadHandler,
)
from pconn.plugin_entries import PluginEntryDisabled, PluginEntryState, UnknownEntry

from . import plugin_entry_flow
from .const import CONFIG_DIR, DATA_LOGGING
from .core import PConn
from .exceptions import PConnError, PluginActionError, UnknownPluginAction
from .helpers import license_file
from .helpers.workstations import WSError

pconn: PConn = None  # type: ignore[assignment]

config_path = os.path.abspath(os.path.join(os.getcwd(), CONFIG_DIR))


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Load Gallagher plugins object."""
    os.makedirs(config_path, exist_ok=True)
    global pconn  # pylint: disable=global-statement
    pconn = PConn(config_path)
    await pconn.async_setup()
    yield
    await pconn.async_stop()


app = FastAPI(lifespan=lifespan)
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sets the templates directory to the `build` folder from `npm run build`
# this is where you'll find the index.html file.
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
templates = Jinja2Templates(directory=frontend_path)

# Mounts the `static` folder within the `build` folder to the `/static` route.
app.mount(
    "/static", StaticFiles(directory=f"{frontend_path}/static", html=True), "static"
)


def run_server() -> None:
    """Launch server."""
    global config_path  # pylint: disable=global-statement
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Web server host", type=str, default="0.0.0.0")
    parser.add_argument("-p", "--port", type=int, default=80)
    parser.add_argument(
        "-c",
        "--config",
        metavar="path_to_config_dir",
        default=config_path,
        help="Directory that contains the Home Assistant configuration",
    )
    args = parser.parse_args()
    config_path = args.config

    uvicorn.run(app, host=args.host, port=args.port)


# region GET methods


@app.get("/api/config/plugins")
def get_plugins() -> dict[str, Any]:
    """Return list of available plugins."""
    # pylint: disable-next=import-outside-toplevel
    from . import interfaces

    response = interfaces.get_interface_descriptions(pconn)
    return {"result": response}


@app.get("/api/config/plugin_entries")
async def return_plugin_entries() -> dict[str, Any]:
    """Return plugin entry config."""
    result = await pconn.plugin_entries.async_entries_by_domain()
    return {"result": result}


@app.get("/api/config/plugin_entries/{entry_id}")
async def get_entry_config(entry_id: str) -> dict[str, Any]:
    """Return plugin entry config."""
    if entry := pconn.plugin_entries.async_get_entry(entry_id):
        return {"result": entry.entry_json()}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found."
    )


@app.get("/api/config/system")
async def return_system_info() -> dict[str, Any]:
    """Return system info."""
    return {"result": pconn.get_system_info()}


@app.get("/api/config/workstations/registered")
def get_registered_workstations(request: Request) -> dict[str, Any]:
    """Return registered workstations."""
    workstations = pconn.workstations.registered_workstations
    current_ws = None
    if request.client:
        current_ws = pconn.workstations.workstation_by_ip(request.client.host)
    return {
        "result": {
            "workstations": workstations,
            "current_ws": current_ws,
        }
    }


@app.get("/api/logs")
async def get_plugin_logs() -> dict[str, Any]:
    """Send the log entries to the frontend."""
    return {"result": pconn.data["logger"].records}


@app.get("/api/logs/download")
async def download_log_file() -> FileResponse:
    """Download the log file."""
    return FileResponse(pconn.data[DATA_LOGGING])


@app.get("/api/state")
async def verify_app_state(request: Request) -> dict[str, Any]:
    """Verify app state."""
    try:
        redirect = await pconn.async_verify_app_state()
    except PConnError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        ) from err
    return {"result": redirect}


@app.get("/api/plugins/workstation_entries")
async def get_plugin_entries_for_ws(
    request: Request,
) -> dict[str, list[dict[str, Any]]]:
    """Return active plugin entries for workstation."""
    ws_name: str | None = None
    if (client := request.client) and (
        ws := pconn.workstations.workstation_by_ip(client.host)
    ):
        ws_name = ws["name"]

    plugin_entries = await pconn.plugin_entries.async_entries_by_domain()
    loaded_entries = []
    for entries in plugin_entries.values():
        loaded_entries.extend(
            [
                entry
                for entry in entries
                if entry.get("state") == PluginEntryState.LOADED
                and entry.get("ws") in [ws_name, None]
            ]
        )
    return {"result": loaded_entries}


@app.get("/api/plugins/{entry_id}")
async def get_plugin_entry_state(entry_id: str) -> dict[str, Any]:
    """Return plugin entry state."""
    if not (entry := pconn.plugin_entries.async_get_entry(entry_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry id {entry_id} not found.",
        )
    if entry.state != PluginEntryState.LOADED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry id {entry_id} not not loaded.",
        )
    return {"result": entry.entry_json()}


@app.get("/api/translations/plugins/{domain}")
async def get_plugin_translations(domain: str) -> dict[str, Any]:
    """Return plugin translation strings for specific category."""
    # pylint: disable-next=import-outside-toplevel
    from .helpers.translations import async_get_translations

    response = await async_get_translations(pconn, [domain])
    return {"result": response}


@app.get("/api/plugins/{entry_id}/stream")
async def stream(entry_id: str) -> StreamingResponse:
    """Stream data from plugin."""
    try:
        event_stream = pconn.plugin_entries.get_event_stream(entry_id)
    except UnknownEntry as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        ) from err
    except PluginEntryDisabled as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except UnknownPluginAction as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        ) from err
    except PluginActionError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/workstation/verify")
def get_workstation(request: Request) -> dict[str, Any]:
    """Return workstation by its ip."""
    if not (client := request.client):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to detect the workstation ip",
        )
    try:
        ws = pconn.workstations.verify_ws_by_ip(client.host)
    except WSError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    return {"result": ws}


# endregion GET methods


# region POST methods
class LoggerConfig(BaseModel):
    """Plugin logging config."""

    component: str
    level: str
    save: bool = False


@app.post("/api/config/logs/set_level", status_code=status.HTTP_202_ACCEPTED)
def set_log_level(log_config: LoggerConfig) -> None:
    """Set the logging level for specific plugin or all."""
    # pylint: disable-next=import-outside-toplevel
    from .util import logger

    log_point = {log_config.component: log_config.level.upper()}

    logger.set_log_levels(log_point)
    if log_config.save:
        pconn.config.update(log_config=log_point)


@app.post("/api/config/logs/reset_levels", status_code=status.HTTP_202_ACCEPTED)
def reset_log_levels() -> None:
    """Set the logging level for specific plugin or all."""
    pconn.config.log_config.clear()
    pconn.config.update()


@dataclass
class PluginFlowPost:
    """Plugin flow post data class."""

    handler: str
    flow_id: str | None = None
    user_input: dict[str, Any] | None = None


@app.post("/api/config/plugin_entries/config/flow")
async def handle_plugin_config_flow(
    data: PluginFlowPost, request: Request
) -> dict[str, Any]:
    """Handle plugin entry config."""
    client = request.client
    assert client is not None
    ws_ip = client.host
    try:
        if data.flow_id is None:
            result = await pconn.plugin_entries.flow.async_init(
                data.handler, data=data.user_input, ws_ip=ws_ip
            )
        else:
            result = await pconn.plugin_entries.flow.async_configure(
                data.flow_id, data.user_input
            )
    except plugin_entry_flow.UnknownHandler as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid handler specified",
        ) from err
    except plugin_entry_flow.UnknownStep as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err
    except plugin_entry_flow.UnknownFlow as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid flow specified",
        ) from err
    flow_result = pconn.plugin_entries.flow.prepare_result_json(result)
    return {"result": flow_result}


@app.post("/api/config/plugin_entries/options/flow")
async def handle_plugin_options_flow(
    data: PluginFlowPost, request: Request
) -> dict[str, Any]:
    """Handle plugin entry options."""
    client = request.client
    assert client is not None
    ws_ip = client.host
    try:
        if data.flow_id is None:
            result = await pconn.plugin_entries.options.async_init(
                data.handler, data=data.user_input, ws_ip=ws_ip
            )
        else:
            result = await pconn.plugin_entries.options.async_configure(
                data.flow_id, data.user_input
            )
    except plugin_entry_flow.InvalidData as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.schema_errors,
        ) from err
    except plugin_entry_flow.UnknownHandler as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid handler specified",
        ) from err
    except plugin_entry_flow.UnknownStep as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err
    except plugin_entry_flow.UnknownFlow as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid flow specified",
        ) from err
    flow_result = pconn.plugin_entries.flow.prepare_result_json(result)
    return {"result": flow_result}


@dataclass
class PluginPost:
    """Plugin post data class."""

    action: str = ""
    user_input: dict[str, Any] = field(default_factory=dict)


@app.post("/api/config/plugin_entries/{entry_id}")
async def handle_plugin_config(entry_id: str, data: PluginPost) -> dict[str, Any]:
    """Handle plugin entry config."""
    if not pconn.plugin_entries.async_get_entry(entry_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="entry_id not found"
        )
    result: dict[str, Any] = {}
    if data.action == "delete":
        result = await pconn.plugin_entries.async_remove(entry_id)
    elif data.action == "reload":
        reload_ok = await pconn.plugin_entries.async_reload(entry_id)
        result = {"result": reload_ok}
    elif data.action == "disable":
        # pylint: disable-next=import-outside-toplevel
        from . import plugin_entries

        if (disabled_by := data.user_input.get("disabled_by")) is not None:
            disabled_by = plugin_entries.ConfigEntryDisabler(disabled_by)
        result = await pconn.plugin_entries.async_set_disabled_by(entry_id, disabled_by)
    return result


@dataclass
class WorkstationPost:
    """Workstation post data class."""

    action: str = ""
    data: dict[str, Any] = field(default_factory=dict)


@app.post("/api/config/workstations")
async def workstation_action(data: WorkstationPost, request: Request) -> None:
    """Perform action for workstation."""
    if not (client := request.client):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot get client ip",
        )

    try:
        if data.action == "register" and (name := data.data.get("name")):
            await pconn.workstations.async_register_ws(
                name, client.host, data.data.get("dashboard_only", False)
            )
        elif ws_id := data.data.get("id"):
            if data.action == "update":
                await pconn.workstations.async_update_ws(
                    ws_id,
                    data.data["name"],
                    data.data["ip_address"],
                    dashboard_only=data.data["dashboard_only"],
                )
            elif data.action == "disable":
                await pconn.workstations.async_set_ws_disabled(
                    ws_id, client.host, data.data["disabled_by"]
                )
            elif data.action == "delete":
                await pconn.workstations.async_remove_ws(ws_id, client.host)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A required field is missing",
            )
    except WSError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@app.post("/api/plugins/{entry_id}")
async def post_plugin_view(entry_id: str, plugin_post: PluginPost) -> dict[str, Any]:
    """Call action from plugin entry instance and return response."""
    try:
        return await pconn.plugin_entries.async_get_view(
            entry_id, plugin_post.action, plugin_post.user_input
        )
    except UnknownEntry as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        ) from err
    except PluginEntryDisabled as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except UnknownPluginAction as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        ) from err
    except PluginActionError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        ) from err


# endregion POST methods


@app.post("/api/file/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    """Upload file to temporary folder."""
    file_upload_handler = FileUploadHandler(pconn)
    file_id = await file_upload_handler.upload_file(file)
    return {"result": file_id}


class FileUploadRequest(BaseModel):
    """File upload data class."""

    file_id: str


@app.post("/api/file/delete")
def delete_file(data: FileUploadRequest) -> None:
    """Remove file from temporary folder."""
    file_upload_data: FileUploadData = pconn.data[FILE_UPLOAD_DOMAIN]
    if file_upload_data.files.pop(data.file_id, None) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    shutil.rmtree(file_upload_data.file_dir(data.file_id))


@app.post("/api/license/apply")
async def apply_license(file: UploadFile = File(...)) -> None:
    """Verify the uploaded license file."""
    file_upload_handler = FileUploadHandler(pconn)
    file_id = await file_upload_handler.upload_file(file)

    try:
        await pconn.async_add_executor_job(
            license_file.validate_uploaded_license, pconn, file_id
        )
    except license_file.LicenseNotValid as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(err)
        ) from err
    await pconn.async_run()


@app.post("/api/license/delete")
async def clear_license() -> None:
    """Remove license file."""
    await pconn.async_add_executor_job(license_file.delete_license, pconn)
    await pconn.async_run()


class ConfigData(BaseModel):
    """Gallagher server config."""

    connection: str
    host: str
    port: int
    api_key: str
    ssl: bool
    token: str | None = None


@app.get("/{path:path}")
async def react_app(req: Request, path: str) -> Response:
    """Define a route handler for `/*` essentially."""
    return templates.TemplateResponse("index.html", {"request": req})


if __name__ == "__main__":
    run_server()
