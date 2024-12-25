"""Abstract class for plugin entry."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Callable, Coroutine, Mapping
from copy import deepcopy
from enum import StrEnum
import logging
import os
from random import getrandbits
from types import MappingProxyType
from typing import Any, Generic, cast

from typing_extensions import TypeVar

from . import interfaces, plugin_entry_flow
from .const import PLUGINS_ENTRIES
from .core import CALLBACK_TYPE, PConn
from .exceptions import (
    PConnError,
    PluginEntryError,
    PluginEntryNotReady,
    UnknownPluginAction,
)
from .setup import async_process_deps_reqs, async_setup_interface
from .util import json as json_util
from .util.decorator import Registry

_LOGGER = logging.getLogger(__name__)

HANDLERS: Registry[str, type[PluginEntryFlow]] = Registry()

_DataT = TypeVar("_DataT", default=Any)
_CallableT = TypeVar("_CallableT", bound=Callable[..., Any])
_R = TypeVar("_R")


class ConfigEntryDisabler(StrEnum):
    """What disabled a config entry."""

    USER = "user"
    WORKSTATION = "workstation"


class ConfigError(PConnError):
    """Error while configuring an plugin entry."""


class UnknownEntry(ConfigError):
    """Unknown entry specified."""


class PluginEntryDisabled(ConfigError):
    """Plugin entry is disabled."""


class PluginEntryState(StrEnum):
    """Represent the current state of a plugin entry."""

    LOADED = "loaded"
    SETUP_ERROR = "setup_error"
    NOT_LOADED = "not_loaded"


UpdateListenerType = Callable[[PConn, "PluginEntry"], Coroutine[Any, Any, None]]


def view(func: _CallableT) -> _CallableT:
    """Register a frontend view."""
    setattr(func, "_view", True)
    return func


def is_view(func: Callable[..., Any]) -> bool:
    """Check if function is registered as a frontend view."""
    return getattr(func, "_view", False) is True


class PluginEntry(Generic[_DataT]):
    """Class representing Plugin entry."""

    data: MappingProxyType[str, Any]
    options: MappingProxyType[str, Any]
    plugin_data: _DataT

    def __init__(
        self,
        domain: str,
        title: str,
        data: Mapping[str, Any],
        ws_id: str | None = None,
        options: Mapping[str, Any] | None = None,
        platform_entries: Mapping[str, Any] | None = None,
        entry_id: str | None = None,
        disabled_by: ConfigEntryDisabler | None = None,
    ) -> None:
        """Initialize a new PluginEntry."""
        self.entry_id = entry_id or "%032x" % getrandbits(32 * 4)
        self.domain = domain
        self.title = title
        self.ws_id = ws_id
        self.data = MappingProxyType(data)
        self.options = MappingProxyType(options or {})
        self.platform_entries = MappingProxyType(platform_entries or {})
        self.state: PluginEntryState = PluginEntryState.NOT_LOADED
        self.disabled_by = disabled_by
        self.interface_for_domain: interfaces.Interface | None = None
        self.reload_lock = asyncio.Lock()
        self._tasks: set[asyncio.Future[Any]] = set()
        self._background_tasks: set[asyncio.Future[Any]] = set()
        self.event_stream: Callable[[], AsyncGenerator[str, None]] | None = None
        self._on_unload: list[Callable[[], Coroutine[Any, Any, None] | None]] | None = (
            None
        )
        self.update_listeners: list[UpdateListenerType] = []
        self.reason: str | None = None

    def add_event_stream(self, target: Callable[[], AsyncGenerator[str, None]]) -> None:
        """Add target to event streams."""
        self.event_stream = target

    def add_update_listener(self, listener: UpdateListenerType) -> CALLBACK_TYPE:
        """Listen for when entry is updated.

        Returns function to unlisten.
        """
        self.update_listeners.append(listener)
        return lambda: self.update_listeners.remove(listener)

    def as_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the plugin entry."""
        return {
            "entry_id": self.entry_id,
            "domain": self.domain,
            "title": self.title,
            "ws_id": self.ws_id,
            "data": dict(self.data),
            "options": dict(self.options),
            "platform_entries": dict(self.platform_entries),
            "disabled_by": self.disabled_by,
        }

    def entry_json(self) -> dict[str, Any]:
        """Return entry json for frontend."""
        handler = HANDLERS.get(self.domain)
        # work out if handler has support for options flow
        supports_options = handler is not None and handler.async_supports_options_flow(
            self
        )
        return {
            "entry_id": self.entry_id,
            "domain": self.domain,
            "title": self.title,
            "ws": self.ws_id,
            "state": self.state,
            "supports_options": supports_options,
            "disabled_by": self.disabled_by,
            "reason": self.reason,
        }

    async def async_setup(
        self,
        pconn: PConn,
        *,
        interface: interfaces.Interface | None = None,
    ) -> None:
        """Setup plugin entry."""
        if self.disabled_by:
            return

        if interface is None:
            try:
                interface = await interfaces.async_get_interface(pconn, self.domain)
            except interfaces.InterfaceNotFound as err:
                _LOGGER.error(
                    "Error getting interface for domain %s: %s",
                    self.domain,
                    err,
                )
                return
        self.interface_for_domain = interface

        try:
            component = interface.get_component()
        except ImportError as err:
            _LOGGER.error(
                "Error importing interface %s to set up %s plugin entry: %s",
                interface.domain,
                self.domain,
                err,
            )
            return

        if self.domain == interface.domain:
            try:
                interface.get_platform("plugin_flow")
            except ImportError as err:
                _LOGGER.error(
                    (
                        "Error importing platform plugin_flow from interface %s to"
                        " set up %s plugin entry: %s"
                    ),
                    interface.domain,
                    self.domain,
                    err,
                )
                self.state = PluginEntryState.SETUP_ERROR
                return

        error_reason = None

        try:
            result = await component.async_setup_entry(pconn, self)
            if not isinstance(result, bool):
                _LOGGER.error(  # type: ignore[unreachable]
                    "%s.async_setup_entry did not return boolean", self.domain
                )
                result = False
        except PluginEntryNotReady as ex:
            error_reason = str(ex) or "Unknown plugin entry not ready error"
            _LOGGER.error(
                "Error setting up entry %s for %s: %s",
                self.title,
                self.domain,
                f"{str(ex)} - [{ex.reason}]",
            )
            result = False
        except PluginEntryError as ex:
            error_reason = str(ex) or "Unknown fatal plugin entry error"
            _LOGGER.exception(
                "Error setting up entry %s for %s: %s",
                self.title,
                self.domain,
                f"{str(ex)} - [{ex.reason}]",
            )
            await self._async_process_on_unload(pconn)
            result = False

        if result:
            self.state = PluginEntryState.LOADED
            self.reason = None
        else:
            self.reason = error_reason
            self.state = PluginEntryState.SETUP_ERROR

    async def async_unload(
        self,
        pconn: PConn,
        *,
        interface: interfaces.Interface | None = None,
    ) -> bool:
        """Unload plugin entry."""
        # This needs to be changed if setup retry is implemented.
        if self.state != PluginEntryState.LOADED:
            self.state = PluginEntryState.NOT_LOADED
            self.reason = None
            return True
        if not interface and (interface := self.interface_for_domain) is None:
            interface = await interfaces.async_get_interface(pconn, self.domain)
        component = interface.get_component()

        try:
            if hasattr(component, "async_unload_entry"):
                await component.async_unload_entry(pconn, self)

            self.state = PluginEntryState.NOT_LOADED
            self.reason = None
            if hasattr(self, "plugin_data"):
                object.__delattr__(self, "plugin_data")
                await self._async_process_on_unload(pconn)
        except Exception as ex:  # pylint: disable=broad-except
            self.reason = str(ex) or "Unknown fatal plugin entry error"
            _LOGGER.exception(
                "Error unloading entry %s for %s: %s",
                self.title,
                self.domain,
                self.reason,
            )
            return False
        return True

    def async_on_unload(
        self, func: Callable[[], Coroutine[Any, Any, None] | None]
    ) -> None:
        """Add a function to call when config entry is unloaded."""
        if self._on_unload is None:
            self._on_unload = []
        self._on_unload.append(func)

    async def _async_process_on_unload(self, pconn: PConn) -> None:
        """Process the on_unload callbacks and wait for pending tasks."""
        if self._on_unload is not None:
            while self._on_unload:
                if job := self._on_unload.pop()():
                    self.async_create_task(pconn, job)

        if not self._tasks and not self._background_tasks:
            return

        cancel_message = f"Config entry {self.title} with {self.domain} unloading"
        for task in self._background_tasks:
            task.cancel(cancel_message)

        _, pending = await asyncio.wait(
            [*self._tasks, *self._background_tasks], timeout=10
        )

        for task in pending:
            _LOGGER.warning(
                "Unloading %s (%s) plugin entry. Task %s did not complete in time",
                self.title,
                self.domain,
                task,
            )

    async def async_get_view(self, view_name: str, kwargs: Any) -> dict[str, Any]:
        """Call the action and return the result."""
        if not (
            (plugin := getattr(self, "plugin_data"))
            and (func := getattr(plugin, view_name, None))
            and is_view(func)
        ):
            error = f"Unknown view {view_name} for plugin entry {self.title}"
            _LOGGER.error(error)
            raise UnknownPluginAction(error)

        if asyncio.iscoroutinefunction(func):
            # If it's an async callable, await its result
            response = await func(**kwargs)
        else:
            # If it's a sync callable, call it directly
            response = func(**kwargs)
        return {"result": response}

    def get_event_stream(self) -> Callable[[], AsyncGenerator[str, None]]:
        """Call the event stream."""
        if not self.event_stream:
            error = f"No event stream for plugin entry {self.title}"
            _LOGGER.error(error)
            raise UnknownPluginAction(error)
        return self.event_stream

    def async_create_task(
        self,
        pconn: PConn,
        target: Coroutine[Any, Any, _R],
        name: str | None = None,
    ) -> asyncio.Task[_R]:
        """Create a task from within the event loop.

        This method must be run in the event loop.

        target: target to call.
        """
        task = pconn.async_create_task(
            target, f"{name} {self.title} {self.domain} {self.entry_id}"
        )
        self._tasks.add(task)
        task.add_done_callback(self._tasks.remove)

        return task

    def async_create_background_task(
        self, pconn: PConn, target: Coroutine[Any, Any, _R], name: str
    ) -> asyncio.Task[_R]:
        """Create a background task tied to the config entry lifecycle.

        Background tasks are automatically canceled when config entry is unloaded.

        target: target to call.
        """
        task = pconn.async_create_background_task(target, name)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.remove)
        return task


class PluginEntryFlow(plugin_entry_flow.FlowHandler):
    """Plugin entry flow class."""

    def __init_subclass__(cls, *, domain: str | None = None, **kwargs: Any) -> None:
        """Initialize a subclass, register if possible."""
        super().__init_subclass__(**kwargs)
        if domain is not None:
            HANDLERS.register(domain)(cls)

    @staticmethod
    def async_get_options_flow(plugin_entry: PluginEntry) -> PluginOptionsFlow:
        """Get the options flow for this handler."""
        raise plugin_entry_flow.UnknownHandler

    @classmethod
    def async_supports_options_flow(cls, plugin_entry: PluginEntry) -> bool:
        """Return options flow support for this handler."""
        return cls.async_get_options_flow is not PluginEntryFlow.async_get_options_flow

    def _async_abort_entries_match(
        self, match_dict: dict[str, Any] | None = None
    ) -> None:
        """Abort if current entries match all data.

        Requires `already_configured` in strings.json in user visible flows.
        """
        if match_dict is None:
            match_dict = {}  # Match any entry
        for entry in self._async_current_entries():
            data_items = entry.data.items()
            for kv in match_dict.items():
                if kv not in data_items:
                    break
            else:
                raise plugin_entry_flow.AbortFlow("already_configured")

    def _abort_if_ws_id_configured(
        self,
        *,
        error: str = "already_configured",
    ) -> None:
        """Abort if the plugin is already configured for this workstation."""
        if self.ws_id is None:
            return

        for entry in self._async_current_entries():
            if entry.ws_id == self.ws_id:
                raise plugin_entry_flow.AbortFlow(error)

    def _async_current_entries(self) -> list[PluginEntry]:
        """Return current entries."""
        return self.pconn.plugin_entries.async_entries(self.handler)

    def limit_reached(self) -> bool:
        """Return true if the license limit has been reached."""
        licensed_plugins = self.pconn.lic_file.licensed_plugins()
        if not (plugin_info := licensed_plugins.get(self.handler)) or not (
            limit := plugin_info.get("limit")
        ):
            return False
        return len(self._async_current_entries()) >= limit

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> plugin_entry_flow.FlowResult:
        """Handle plugin onboarding."""
        platform_labels = ""
        if platforms := getattr(self, "PLATFORMS", None):
            platform_labels = ", ".join(platforms).upper().replace("_", " ")
        return self.async_show_form(
            step_id="init",
            description_placeholders={"platforms": platform_labels},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> plugin_entry_flow.FlowResult:
        """Handle a flow initiated by the user."""
        return self.async_abort(reason="not_implemented")


class PluginOptionsFlow(plugin_entry_flow.FlowHandler):
    """Base class for options flows with plugin entry and options."""

    def __init__(self, plugin_entry: PluginEntry) -> None:
        """Initialize options flow."""
        self._plugin_entry = plugin_entry
        self._options = deepcopy(dict(plugin_entry.options))

    @property
    def plugin_entry(self) -> PluginEntry:
        """Return the config entry."""
        return self._plugin_entry


class PluginEntires:
    """Manager plugin entries."""

    def __init__(self, pconn: PConn) -> None:
        """Initialize the plugin entries manager."""
        self.pconn = pconn
        self.flow = PluginEntriesFlowManager(pconn, self)
        self.options = OptionsFlowManager(pconn)
        self._entries: dict[str, PluginEntry] = {}
        self._domain_index: dict[str, list[str]] = {}

    def async_domains(self) -> list[str]:
        """Return plugin domains which have entries."""
        return list({entry.domain: None for entry in self._entries.values()})

    def async_get_entry(self, entry_id: str) -> PluginEntry | None:
        """Return entry matching entry_id."""
        return self._entries.get(entry_id)

    def async_entries(self, domain: str | None = None) -> list[PluginEntry]:
        """Return all entries or entries for a specific domain."""
        if domain is None:
            return list(self._entries.values())
        return [
            self._entries[entry_id] for entry_id in self._domain_index.get(domain, [])
        ]

    async def async_entries_by_domain(self) -> dict[str, list[dict[str, Any]]]:
        """Return all entries grouped by domain."""
        entry_not_ready = False
        entries: dict[str, list[dict[str, Any]]] = {}
        plugin_interfaces = interfaces.get_interface_descriptions(self.pconn)["plugins"]
        for domain, entry_ids in sorted(self._domain_index.items(), key=lambda x: x[0]):
            if entry_not_ready:
                break
            if domain not in plugin_interfaces:
                continue
            for entry_id in entry_ids:
                if self._entries[entry_id].reload_lock.locked():
                    entry_not_ready = True
                    break
                entry = self._entries[entry_id].entry_json()
                if ws := self.pconn.workstations.async_get_workstation(entry["ws"]):
                    entry["ws"] = ws["name"]
                entries.setdefault(domain, []).append(entry)
        if entry_not_ready:
            await asyncio.sleep(0.1)
            return await self.async_entries_by_domain()
        return entries

    def async_entries_for_ws(
        self, ws_id: str, domain: str | None = None
    ) -> list[PluginEntry]:
        """Return all entries for workstation."""
        ws_entries = [entry for entry in self._entries.values() if entry.ws_id == ws_id]
        if domain is not None:
            return [entry for entry in ws_entries if entry.domain == domain]
        return ws_entries

    async def _async_save_data(self) -> None:
        """Save entry data to file."""
        await self.pconn.async_add_executor_job(self._write_data)

    def _write_data(self) -> None:
        """Write data to file."""
        path = self.pconn.config.path(PLUGINS_ENTRIES)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json_util.save_json(
            path,
            self._data_to_save(),
        )

    def _data_to_save(self) -> dict[str, list[dict[str, Any]]]:
        """Return data to save."""
        return {"entries": [entry.as_dict() for entry in self._entries.values()]}

    async def async_add(self, entry: PluginEntry) -> None:
        """Add and setup plugin entry."""
        if entry.entry_id in self._entries:
            raise PluginEntryError("An entry with id {entry.entry_id} already exists.")
        self._entries[entry.entry_id] = entry
        self._domain_index.setdefault(entry.domain, []).append(entry.entry_id)
        await self.async_setup(entry.entry_id)
        await self._async_save_data()

    async def async_remove(self, entry_id: str) -> dict[str, Any]:
        """Remove an entry."""
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        unload_success = await self.async_unload(entry_id)
        for p_domain, p_entry_id in entry.platform_entries.items():
            self._domain_index[p_domain].remove(p_entry_id)
            del self._entries[p_entry_id]
            if not self._domain_index[p_domain]:
                del self._domain_index[p_domain]
        del self._entries[entry.entry_id]
        self._domain_index[entry.domain].remove(entry.entry_id)
        if not self._domain_index[entry.domain]:
            del self._domain_index[entry.domain]
        await self._async_save_data()
        return {"result": unload_success}

    async def async_initialize(self) -> None:
        """Initialize plugin entries from config."""
        entries_path = self.pconn.config.path(PLUGINS_ENTRIES)
        config = cast(
            dict[str, list[dict[str, Any]]], json_util.load_json(entries_path)
        )

        if not config:
            self._entries = {}
            self._domain_index = {}
            return

        entries: dict[str, PluginEntry] = {}
        domain_index: dict[str, list[str]] = {}

        config_entries: list[dict[str, Any]] = config["entries"]  # fix this error
        for entry in config_entries:
            domain = entry["domain"]
            entry_id = entry["entry_id"]

            entries[entry_id] = PluginEntry(
                domain=domain,
                entry_id=entry_id,
                ws_id=entry.get("ws_id"),
                title=entry["title"],
                data=entry["data"],
                options=entry.get("options"),
                platform_entries=entry.get("platform_entries"),
                disabled_by=ConfigEntryDisabler(entry["disabled_by"])
                if entry.get("disabled_by")
                else None,
            )
            domain_index.setdefault(domain, []).append(entry_id)

        self._domain_index = domain_index
        self._entries = entries

    async def async_setup(self, entry_id: str) -> bool:
        """Set up a config entry.

        Return True if entry has been successfully loaded.
        """
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        if entry.state is not PluginEntryState.NOT_LOADED:
            raise PluginEntryError(
                f"The plugin entry {entry.title} ({entry.domain}) with entry_id"
                f" {entry.entry_id} cannot be setup because is already loaded in the"
                f" {entry.state} state"
            )
        if entry.domain in self.pconn.config.interfaces:
            await entry.async_setup(self.pconn)
        # verify that the else section works
        else:
            # Setting up the interface will set up all its plugin entries
            result = await async_setup_interface(self.pconn, entry.domain)

            if not result:
                return result

        return (
            entry.state is PluginEntryState.LOADED  # type: ignore[comparison-overlap]
        )

    async def async_unload(self, entry_id: str) -> bool:
        """Unload a plugin entry."""
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry
        unload_result = await entry.async_unload(self.pconn)
        for p_entry_id in entry.platform_entries.values():
            if (p_entry := self.async_get_entry(p_entry_id)) is None:
                raise UnknownEntry
            unload_result = await p_entry.async_unload(self.pconn)
        return unload_result

    async def async_reload(self, entry_id: str) -> bool:
        """Reload an entry.

        If an entry was not loaded, will just load.
        """
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        async with entry.reload_lock:
            unload_result = await self.async_unload(entry_id)

            if not unload_result or entry.disabled_by:
                return unload_result

            return await self.async_setup(entry_id)

    async def async_set_disabled_by(
        self, entry_id: str, disabled_by: ConfigEntryDisabler | None
    ) -> dict[str, bool]:
        """Disable an entry.

        If disabled_by is changed, the config entry will be reloaded.
        """
        result = False
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry

        if entry.disabled_by is disabled_by:
            result = True

        entry.disabled_by = disabled_by
        await self._async_save_data()

        result = await self.async_reload(entry_id)
        return {"result": result}

    async def async_get_view(
        self, entry_id: str, action: str, user_input: dict[str, Any]
    ) -> dict[str, Any]:
        """Call the action and return the result."""
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry(f"plugin entry_id {entry_id} does not exist")
        if entry.disabled_by:
            raise PluginEntryDisabled(f"plugin entry {entry_id} is disabled")
        response = await entry.async_get_view(action, user_input)
        return response

    def get_event_stream(
        self, entry_id: str
    ) -> Callable[[], AsyncGenerator[str, None]]:
        """Call the action and return the result."""
        if (entry := self.async_get_entry(entry_id)) is None:
            raise UnknownEntry(f"plugin entry_id {entry_id} does not exist")
        if entry.disabled_by:
            raise PluginEntryDisabled(f"plugin entry {entry_id} is disabled")
        return entry.get_event_stream()

    async def async_get_platform_entry(
        self, entry: PluginEntry, platform: str
    ) -> PluginEntry | None:
        """Return a plugin entry for a platform."""

        if (entry_id := entry.platform_entries.get(platform)) and (
            platform_entry := self.async_get_entry(entry_id)
        ):
            if (
                platform_entry.state == PluginEntryState.LOADED
                or await self.async_setup(platform_entry.entry_id)
            ):
                return platform_entry
        return None

    def async_update_entry(
        self,
        entry: PluginEntry,
        *,
        data: Mapping[str, Any] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> bool:
        """Update a plugin entry."""
        changed = False

        # this is not used for now. Maybe implement reauth later
        if data is not None and entry.data != data:
            changed = True
            entry.data = MappingProxyType(data)

        # this is not used now. Can be used if plugin is updated
        if options is not None and entry.options != options:
            changed = True
            entry.options = MappingProxyType(options)
        if not changed:
            return False

        for listener in entry.update_listeners:
            self.pconn.async_create_task(
                listener(self.pconn, entry),
                f"plugin entry update listener {entry.title} {entry.domain}",
            )

        self._write_data()
        return True


class PluginEntriesFlowManager(plugin_entry_flow.FlowManager):
    """Manage plugin entries flows."""

    def __init__(self, pconn: PConn, plugin_entries: PluginEntires) -> None:
        """Initialize plugin entries flow manager."""
        super().__init__(pconn)
        self.plugin_entries = plugin_entries
        self._progress: dict[str, plugin_entry_flow.FlowHandler] = {}

    async def async_init(
        self,
        handler: str,
        *,
        ws_ip: str | None = None,
        parent_flow_id: str | None = None,
        data: Any = None,
    ) -> plugin_entry_flow.FlowResult:
        """Start a configuration flow."""
        flow = await self.async_create_flow(handler)
        if not flow:
            raise plugin_entry_flow.UnknownFlow("Flow was not created")
        flow.pconn = self.pconn
        flow.handler = handler
        flow.platform_entries = {}
        flow.flow_id = "%032x" % getrandbits(32 * 4)
        flow.parent_flow_id = parent_flow_id
        if flow.PER_WS:
            if ws_ip is None or not (
                ws := self.pconn.workstations.workstation_by_ip(ws_ip)
            ):
                raise plugin_entry_flow.UnknownWorkstation(
                    "Workstation is not registered"
                )
            flow.ws_id = ws["id"]
        self._progress[flow.flow_id] = flow

        # Check if the license limit has been reached
        if flow.limit_reached():
            return flow.async_abort(reason="license_limit_reached")

        result = await self._async_handle_step(flow, flow.init_step, data)
        return result

    async def async_configure(
        self, flow_id: str, user_input: dict | None = None
    ) -> plugin_entry_flow.FlowResult:
        """Continue a data entry flow."""
        if (flow := self._progress.get(flow_id)) is None:
            raise plugin_entry_flow.UnknownFlow
        for platform in flow.PLATFORMS:
            if platform not in flow.platform_entries:
                return await super().async_init(platform, parent_flow_id=flow.flow_id)
        return await super().async_configure(flow_id, user_input)

    async def async_create_flow(self, handler_key: str) -> PluginEntryFlow:
        """Creates a plugin flow for the given domain."""
        handler = await _async_get_flow_handler(self.pconn, handler_key)
        flow = handler()
        return flow

    async def async_finish_flow(
        self, flow: plugin_entry_flow.FlowHandler, result: plugin_entry_flow.FlowResult
    ) -> plugin_entry_flow.FlowResult:
        """Finish a config flow and add an entry."""
        flow = cast(PluginEntryFlow, flow)

        if result["type"] != plugin_entry_flow.FlowResultType.CREATE_ENTRY:
            return result

        entry = PluginEntry(
            domain=result["handler"],
            title=result["title"],
            data=result["data"],
            ws_id=flow.ws_id,
            platform_entries=flow.platform_entries,
        )
        await self.plugin_entries.async_add(entry)
        result["result"] = entry
        if flow.parent_flow_id and (
            parent_flow := self._progress.get(flow.parent_flow_id)
        ):
            parent_flow.platform_entries[entry.domain] = entry.entry_id
            assert parent_flow.cur_step
            parent_flow.cur_step["step_id"] = "user"
            return await self.async_configure(parent_flow.flow_id)
        return result


class OptionsFlowManager(plugin_entry_flow.FlowManager):
    """Flow to set options for a configuration entry."""

    def _async_get_plugin_entry(self, plugin_entry_id: str) -> PluginEntry:
        """Return plugin entry or raise if not found."""
        entry = self.pconn.plugin_entries.async_get_entry(plugin_entry_id)
        if entry is None:
            raise UnknownEntry(plugin_entry_id)

        return entry

    async def async_create_flow(
        self,
        handler_key: str,
    ) -> PluginOptionsFlow:
        """Create an options flow for a plugin entry.

        Entry_id and flow.handler is the same thing to map entry with flow.
        """
        entry = self._async_get_plugin_entry(handler_key)
        handler = await _async_get_flow_handler(self.pconn, entry.domain)
        return handler.async_get_options_flow(entry)

    async def async_finish_flow(
        self, flow: plugin_entry_flow.FlowHandler, result: plugin_entry_flow.FlowResult
    ) -> plugin_entry_flow.FlowResult:
        """Finish an options flow and update options for plugin entry.

        Flow.handler and entry_id is the same thing to map flow with entry.
        """
        flow = cast(PluginOptionsFlow, flow)

        if result["type"] != plugin_entry_flow.FlowResultType.CREATE_ENTRY:
            return result

        entry = self.pconn.plugin_entries.async_get_entry(flow.handler)
        if entry is None:
            raise UnknownEntry(flow.handler)
        if result["data"] is not None:
            self.pconn.plugin_entries.async_update_entry(entry, options=result["data"])

        result["result"] = True
        return result


async def _load_interface(pconn: PConn, domain: str) -> None:
    try:
        interface = await interfaces.async_get_interface(pconn, domain)
    except interfaces.InterfaceNotFound as err:
        _LOGGER.error("Cannot find interface %s", domain)
        raise plugin_entry_flow.UnknownHandler from err

    await async_process_deps_reqs(pconn, interface)

    try:
        interface.get_platform("plugin_flow")
    except ImportError as err:
        _LOGGER.error(
            "Error occurred loading flow for integration %s: %s",
            domain,
            err,
        )
        raise plugin_entry_flow.UnknownHandler


async def _async_get_flow_handler(pconn: PConn, domain: str) -> type[PluginEntryFlow]:
    """Get a flow handler for specified domain."""

    # First check if there is a handler registered for the domain
    if handler := HANDLERS.get(domain):
        return handler

    await _load_interface(pconn, domain)

    if handler := HANDLERS.get(domain):
        return handler

    raise plugin_entry_flow.UnknownHandler
