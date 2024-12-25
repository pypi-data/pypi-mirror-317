"""Class for plugin entry flow."""

from __future__ import annotations

import abc
from collections.abc import Container, Mapping
from enum import StrEnum
from random import getrandbits
from typing import Any, Required, TypedDict

import voluptuous as vol
import voluptuous_serialize

from .core import PConn
from .exceptions import PConnError
from .helpers.selector import custom_serializer


class FlowError(PConnError):
    """Base class for data entry errors."""


class UnknownHandler(FlowError):
    """Unknown handler specified."""


class UnknownFlow(FlowError):
    """Unknown flow specified."""


class UnknownStep(FlowError):
    """Unknown step specified."""


# ignore misc is required as vol.Invalid is not typed
# mypy error: Class cannot subclass "Invalid" (has type "Any")
class InvalidData(vol.Invalid):  # type: ignore[misc]
    """Invalid data provided."""

    def __init__(
        self,
        message: str,
        path: list[str | vol.Marker] | None,
        error_message: str | None,
        schema_errors: dict[str, Any],
        **kwargs: Any,
    ) -> None:
        """Initialize an invalid data exception."""
        super().__init__(message, path, error_message, **kwargs)
        self.schema_errors = schema_errors


class UnknownWorkstation(FlowError):
    """Unknown workstation."""


class AbortFlow(FlowError):
    """Exception to indicate a flow needs to be aborted."""

    def __init__(self, reason: str) -> None:
        """Initialize an abort flow exception."""
        super().__init__(f"Flow aborted: {reason}")
        self.reason = reason


class FlowResultType(StrEnum):
    """Result type for a data entry flow."""

    FORM = "form"
    CREATE_ENTRY = "create_entry"
    ABORT = "abort"
    MENU = "menu"


class FlowResult(TypedDict, total=False):
    """Typed result dict."""

    data_schema: vol.Schema | None
    data: Mapping[str, Any]
    description: str | None
    description_placeholders: Mapping[str, str | None] | None
    errors: dict[str, str] | None
    flow_id: Required[str]
    handler: Required[str]
    parent_flow: dict[str, str] | None
    last_step: bool | None
    menu_options: Container[str]
    options: Mapping[str, Any]
    step_id: str
    title: str
    type: FlowResultType
    reason: str
    result: Any
    ws_id: str | None


class FlowHandler:
    """Base class for plugin flows."""

    cur_step: FlowResult | None = None
    parent_flow_id: str | None = None
    flow_id: str = None  # type: ignore[assignment]
    pconn: PConn = None  # type: ignore[assignment]
    handler: str = None  # type: ignore[assignment]
    platform_entries: dict[str, str] = None  # type: ignore[assignment]
    ws_id: str | None = None
    init_step = "init"

    PER_WS = False
    PLATFORMS: list[str] = []

    def async_show_form(
        self,
        *,
        step_id: str,
        data_schema: vol.Schema | None = None,
        errors: dict[str, str] | None = None,
        description_placeholders: Mapping[str, str | None] | None = None,
        last_step: bool | None = None,
    ) -> FlowResult:
        """Return plugin settings dict."""
        return FlowResult(
            type=FlowResultType.FORM,
            flow_id=self.flow_id,
            handler=self.handler,
            step_id=step_id,
            data_schema=data_schema,
            errors=errors,
            description_placeholders=description_placeholders,
            last_step=last_step,  # Display next or submit button in frontend
        )

    def async_show_menu(
        self,
        *,
        step_id: str | None = None,
        menu_options: Container[str],
        description_placeholders: Mapping[str, str] | None = None,
    ) -> FlowResult:
        """Show a navigation menu to the user.

        Options dict maps step_id => i18n label
        The step_id parameter is deprecated and will be removed in a future release.
        """
        flow_result = FlowResult(
            type=FlowResultType.MENU,
            flow_id=self.flow_id,
            handler=self.handler,
            data_schema=vol.Schema({"next_step_id": vol.In(menu_options)}),
            menu_options=menu_options,
            description_placeholders=description_placeholders,
        )
        if step_id is not None:
            flow_result["step_id"] = step_id
        return flow_result

    def async_create_entry(
        self,
        *,
        title: str | None = None,
        data: Mapping[str, Any],
        description: str | None = None,
        ws_id: str | None = None,
    ) -> FlowResult:
        """Finish flow."""
        flow_result = FlowResult(
            type=FlowResultType.CREATE_ENTRY,
            flow_id=self.flow_id,
            handler=self.handler,
            data=data,
            description=description,
            ws_id=ws_id,
        )
        if title is not None:
            flow_result["title"] = title
        return flow_result

    def async_abort(
        self,
        *,
        reason: str,
    ) -> FlowResult:
        """Abort the flow."""
        return _create_abort_data(self.flow_id, self.handler, reason)


class FlowManager(abc.ABC):
    """Manage all the flows that are in progress."""

    def __init__(
        self,
        pconn: PConn,
    ) -> None:
        """Initialize the flow manager."""
        self.pconn = pconn
        self._preview: set[str] = set()
        self._progress: dict[str, FlowHandler] = {}
        self._handler_progress_index: dict[str, set[str]] = {}
        self._init_data_process_index: dict[type, set[str]] = {}

    @abc.abstractmethod
    async def async_create_flow(
        self,
        handler_key: str,
    ) -> FlowHandler:
        """Create a flow for specified handler.

        Handler key is the domain of the component that we want to set up.
        """

    @abc.abstractmethod
    async def async_finish_flow(
        self, flow: FlowHandler, result: FlowResult
    ) -> FlowResult:
        """Finish a data entry flow."""

    async def async_init(
        self,
        handler: str,
        *,
        parent_flow_id: str | None = None,
        ws_ip: str | None = None,
        data: Any = None,
    ) -> FlowResult:
        """Start a data entry flow."""
        flow = await self.async_create_flow(handler)
        if not flow:
            raise UnknownFlow("Flow was not created")
        flow.pconn = self.pconn
        flow.handler = handler
        flow.parent_flow_id = parent_flow_id
        flow.flow_id = "%032x" % getrandbits(32 * 4)
        self._progress[flow.flow_id] = flow

        result = await self._async_handle_step(flow, flow.init_step, data)

        return result

    async def async_configure(
        self, flow_id: str, user_input: dict | None = None
    ) -> FlowResult:
        """Continue a data entry flow."""
        if (flow := self._progress.get(flow_id)) is None:
            raise UnknownFlow
        cur_step = flow.cur_step
        assert cur_step is not None

        if (
            data_schema := cur_step.get("data_schema")
        ) is not None and user_input is not None:
            try:
                user_input = data_schema(user_input)
            except vol.Invalid as ex:
                raised_errors = [ex]
                if isinstance(ex, vol.MultipleInvalid):
                    raised_errors = ex.errors
                schema_errors: dict[str, Any] = {}
                for error in raised_errors:
                    try:
                        _map_error_to_schema_errors(schema_errors, error, data_schema)
                    except ValueError:
                        # If we get here, the path in the exception does not exist in the schema.
                        schema_errors.setdefault("base", []).append(str(error))
                raise InvalidData(
                    "Schema validation failed",
                    path=ex.path,
                    error_message=ex.error_message,
                    schema_errors=schema_errors,
                ) from ex

        # Handle a menu navigation choice
        if cur_step["type"] == FlowResultType.MENU and user_input:
            result = await self._async_handle_step(
                flow, user_input["next_step_id"], None
            )
        else:
            result = await self._async_handle_step(
                flow, cur_step["step_id"], user_input
            )

        return result

    def async_abort(self, flow_id: str) -> None:
        """Abort a flow."""
        self._progress.pop(flow_id, None)

    async def _async_handle_step(
        self, flow: FlowHandler, step_id: str, user_input: dict | None
    ) -> FlowResult:
        """Handle a step of a flow."""
        method = f"async_step_{step_id}"

        if not hasattr(flow, method):
            del self._progress[flow.flow_id]
            raise UnknownStep(
                f"Handler {flow.__class__.__name__} doesn't support step {step_id}"
            )

        try:
            result: FlowResult = await getattr(flow, method)(user_input)
        except AbortFlow as err:
            result = _create_abort_data(flow.flow_id, flow.handler, err.reason)
        if result["type"] in [FlowResultType.FORM, FlowResultType.MENU]:
            flow.cur_step = result
            return result
        result = await self.async_finish_flow(flow, result.copy())

        # _async_finish_flow may change result type, check it again
        if result["type"] == FlowResultType.FORM:
            flow.cur_step = result
            return result

        # Abort and Success results both finish the flow
        del self._progress[flow.flow_id]

        return result

    def prepare_result_json(self, result: FlowResult) -> FlowResult:
        """Convert result to JSON."""
        if result["type"] == FlowResultType.CREATE_ENTRY:
            data = result.copy()
            data.pop("result")
            data.pop("data")
            return data

        if "data_schema" not in result:
            return result

        data = result.copy()

        if (schema := data["data_schema"]) is None:
            data["data_schema"] = []
        else:
            data["data_schema"] = voluptuous_serialize.convert(
                schema, custom_serializer=custom_serializer
            )

        return data


def _map_error_to_schema_errors(
    schema_errors: dict[str, Any],
    error: vol.Invalid,
    data_schema: vol.Schema,
) -> None:
    """Map an error to the correct position in the schema_errors.

    Raises ValueError if the error path could not be found in the schema.
    Limitation: Nested schemas are not supported and a ValueError will be raised.
    """
    schema = data_schema.schema
    error_path = error.path
    if not error_path or (path_part := error_path[0]) not in schema:
        raise ValueError("Could not find path in schema")

    if len(error_path) > 1:
        raise ValueError("Nested schemas are not supported")

    # path_part can also be vol.Marker, but we need a string key
    path_part_str = str(path_part)
    schema_errors[path_part_str] = error.error_message


def _create_abort_data(
    flow_id: str,
    handler: str,
    reason: str,
) -> FlowResult:
    """Return the definition of an external step for the user to take."""
    return FlowResult(
        type=FlowResultType.ABORT,
        flow_id=flow_id,
        handler=handler,
        reason=reason,
    )
