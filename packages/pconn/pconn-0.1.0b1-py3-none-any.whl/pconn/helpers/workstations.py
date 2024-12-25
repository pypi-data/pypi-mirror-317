"""Helper to handle workstations."""

from __future__ import annotations

import asyncio
import logging
import os
from random import getrandbits
from typing import Any, NotRequired, TypedDict, cast

from pconn import plugin_entries
from pconn.core import PConn
from pconn.exceptions import PConnError
from pconn.util import json as json_util

WORKSTATIONS = "workstations"

_LOGGER = logging.getLogger(__name__)


class WSError(PConnError):
    """Workstation base error."""


class WSRegisteredError(WSError):
    """Raise exception if workstation already exists."""


class WSLimitError(WSError):
    """Raise exception if workstations limit is reached."""


class WSNotFoundError(WSError):
    """Raise exception if workstation is not found."""


class Workstation(TypedDict):
    """Class representing workstation machine."""

    id: str
    ip: NotRequired[str]
    name: str
    disabled: NotRequired[bool]
    dashboard_only: NotRequired[bool]


class Workstations:
    """Manager Workstations."""

    def __init__(self, pconn: PConn) -> None:
        """Initialize workstations manager."""
        self.pconn = pconn
        self._workstations: dict[str, Workstation] = {}

    @property
    def registered_workstations(self) -> list[Workstation]:
        """Return list of registered workstations."""
        return list(self._workstations.values())

    @property
    def limit_reached(self) -> bool:
        """Return true if the num of registered workstations reached the limit."""
        return len(self._workstations) >= self.pconn.lic_file.license["workstations"]

    async def async_initialize(self) -> None:
        """Initialize workstations from config."""
        ws_path = self.pconn.config.path(WORKSTATIONS)
        config = cast(dict[str, list[dict[str, Any]]], json_util.load_json(ws_path))

        if not config:
            self._workstations = {}
            return

        workstations: dict[str, Workstation] = {}

        workstations = {
            entry["id"]: Workstation(
                id=entry["id"],
                ip=entry["ip"],
                name=entry["name"],
                disabled=entry.get("disabled", False),
                dashboard_only=entry.get("dashboard_only", False),
            )
            for entry in config["workstations"]
        }

        self._workstations = workstations

    def async_get_workstation(self, ws_id: str) -> Workstation | None:
        """Return workstation matching ws_id."""
        return self._workstations.get(ws_id)

    def verify_ws_by_ip(self, ws_ip: str | None) -> Workstation | None:
        """Check the workstation based on ip."""
        if ws_ip is None:
            raise WSError("Can't detect workstation IP")
        if ws := self.workstation_by_ip(ws_ip):
            if self.limit_reached:
                raise WSLimitError("Workstations limit reached.")
            if ws.get("disabled"):
                raise WSError("Workstation is disabled")
        return ws

    def workstation_by_ip(self, ip: str) -> Workstation | None:
        """Return workstation item from ip."""
        for ws in self._workstations.values():
            if ws["ip"] == ip:
                return ws
        return None

    async def _async_save_data(self) -> None:
        """Save entry data to file."""
        await self.pconn.async_add_executor_job(self._write_data)

    def _write_data(self) -> None:
        """Write data to file."""
        path = self.pconn.config.path(WORKSTATIONS)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json_util.save_json(
            path,
            self._data_to_save(),
        )

    def _data_to_save(self) -> dict[str, list[Workstation]]:
        """Return data to save."""
        return {"workstations": list(self._workstations.values())}

    async def async_register_ws(
        self, name: str, ip: str, dashboard_only: bool = False
    ) -> None:
        """Register a new workstation."""
        if self.workstation_by_ip(ip) is not None:
            raise WSRegisteredError(f"A Workstation is already registered with ip {ip}")
        if any(ws["name"] == name for ws in self._workstations.values()):
            raise WSRegisteredError("A workstation with the same name already exists.")
        if len(self._workstations) == self.pconn.lic_file.license["workstations"]:
            raise WSLimitError("Workstations license limit is reached.")
        ws_id = "%032x" % getrandbits(32 * 4)
        self._workstations[ws_id] = Workstation(
            id=ws_id, name=name, ip=ip, dashboard_only=dashboard_only
        )
        _LOGGER.info("Workstation with id {ws_id} successfully registered.")
        await self._async_save_data()

    async def async_update_ws(
        self, ws_id: str, name: str, ws_ip: str, dashboard_only: bool = False
    ) -> None:
        """Update existing workstation to new ip."""
        if not (ws := self._workstations.get(ws_id)):
            raise WSNotFoundError(f"Workstation with id {ws_id} does not exist.")
        if ws["ip"] != ws_ip and any(
            ws["ip"] == ws_ip for ws in self._workstations.values()
        ):
            raise WSRegisteredError(
                "Another workstation with the same ip already exists."
            )
        if ws["name"] != name and any(
            ws["name"] == name for ws in self._workstations.values()
        ):
            raise WSRegisteredError("A workstation with the same name already exists.")
        ws["name"] = name
        ws["ip"] = ws_ip
        ws["dashboard_only"] = dashboard_only
        await self._async_save_data()

    async def async_set_ws_disabled(
        self, ws_id: str, ws_ip: str, disabled_by: str | None
    ) -> None:
        """Enable/Disable workstation."""
        if not (ws := self._workstations.get(ws_id)):
            raise WSNotFoundError(f"Workstation with id {ws_id} does not exist.")
        if disabled_by is not None:
            if (current_ws := self.workstation_by_ip(ws_ip)) and current_ws[
                "id"
            ] == ws_id:
                raise WSError("Disabling this entry is not allowed from this machine.")
            disabled_by = plugin_entries.ConfigEntryDisabler(disabled_by)
        ws["disabled"] = bool(disabled_by)
        if ws_entries := self.pconn.plugin_entries.async_entries_for_ws(ws_id):
            await asyncio.gather(
                *(
                    self.pconn.plugin_entries.async_set_disabled_by(
                        entry.entry_id, disabled_by
                    )
                    for entry in ws_entries
                )
            )
        await self._async_save_data()

    async def async_remove_ws(self, ws_id: str, ws_ip: str) -> None:
        """Remove workstation and associated plugin entries."""
        if ws_id not in self._workstations:
            raise WSNotFoundError(f"Workstation with id {ws_id} does not exist.")
        if (current_ws := self.workstation_by_ip(ws_ip)) and current_ws["id"] == ws_id:
            raise WSError("Disabling this entry is not allowed from this machine.")
        if ws_entries := self.pconn.plugin_entries.async_entries_for_ws(ws_id):
            await asyncio.gather(
                *(
                    self.pconn.plugin_entries.async_remove(entry.entry_id)
                    for entry in ws_entries
                )
            )
        del self._workstations[ws_id]
        await self._async_save_data()
