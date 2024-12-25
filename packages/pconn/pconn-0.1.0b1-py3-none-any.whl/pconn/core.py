"""Gallagher plugins core class."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine, Mapping
from enum import StrEnum
import logging
import logging.handlers
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, TypeVar, cast

from pconn.exceptions import PConnError

from .const import CORE_CONFIG, VERSION
from .helpers import file_upload, license_file
from .util import json as json_util

if TYPE_CHECKING:
    from .helpers.license_file import LicenseFile

_LOGGER = logging.getLogger(__name__)

_R = TypeVar("_R")
_T = TypeVar("_T")

CALLBACK_TYPE = Callable[[], None]


class CoreState(StrEnum):
    """Represent the current state of GllPlugins."""

    not_running = "NOT_RUNNING"
    running = "RUNNING"
    starting = "STARTING"
    stopping = "STOPPING"
    stopped = "STOPPED"
    not_licensed = "NOT_LICENSED"


class ConfigSource(StrEnum):
    """Source of core configuration."""

    DEFAULT = "default"
    STORAGE = "storage"


class GallagherConfig(TypedDict, total=False):
    """Gallagher server config."""

    api_key: str
    cloud_gateway: NotRequired[str]
    host: NotRequired[str]
    port: NotRequired[int]
    ssl: NotRequired[bool]
    token: NotRequired[str]


class Config:
    """Configuration class for Gallagher Plugins."""

    def __init__(self, pconn: PConn, config_dir: str) -> None:
        """Initialize a new config object."""
        self.pconn = pconn
        self.source: ConfigSource = ConfigSource.DEFAULT
        # self.site_name: str = ""
        self.version = VERSION
        self.config_dir: str = config_dir
        self.interfaces: set[str] = set()
        self.log_config: dict[str, str] = {}

    def as_dict(self) -> dict[str, Any]:
        """Create a dictionary representation of the configuration."""
        return {
            "version": self.version,
            "log_config": self.log_config,
        }

    def path(self, *path: str) -> str:
        """Generate path to the file within the configuration directory.

        Async friendly.
        """
        return os.path.join(self.config_dir, *path)

    def _write_data(self) -> None:
        """Write config to file."""
        path = self.path(CORE_CONFIG)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json_util.save_json(
            path,
            self.as_dict(),
        )

    def _update(
        self,
        *,
        source: ConfigSource,
        version: str | None = None,
        log_config: Mapping[str, str] | None = None,
    ) -> None:
        """Update config from dictionary."""
        self.source = source
        if version is not None:
            self.version = version
        if log_config is not None:
            self.log_config.update(log_config)

    def load(self) -> None:
        """Load Gallagher plugins core config."""
        if data := cast(dict[str, Any], json_util.load_json(self.path(CORE_CONFIG))):
            self._update(
                source=ConfigSource.STORAGE,
                version=data.get("version"),
                log_config=data.get("log_config"),
            )

    def update(self, **kwargs: Any) -> None:
        """Update configuration from a dictionary."""
        self._update(source=ConfigSource.STORAGE, **kwargs)
        self._write_data()


class PConn:
    """Platform Connectors class."""

    lic_file: LicenseFile = None  # type: ignore[assignment]

    def __init__(self, config_dir: str) -> None:
        """Initialize class."""

        # pylint: disable-next=import-outside-toplevel
        from . import plugin_entries

        # pylint: disable-next=import-outside-toplevel
        from .helpers.workstations import Workstations

        self.loop = asyncio.get_running_loop()
        self._tasks: set[asyncio.Future[Any]] = set()
        self._background_tasks: set[asyncio.Future[Any]] = set()
        self.states: dict[str, plugin_entries.PluginEntryState] = {}
        self.config = Config(self, config_dir)
        self.config.load()
        self.data: dict[str, Any] = {}
        self.state: CoreState = CoreState.not_running
        self.plugin_entries = plugin_entries.PluginEntires(self)
        self.workstations = Workstations(self)

    def async_add_executor_job(
        self, target: Callable[..., _T], *args: Any
    ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        task = self.loop.run_in_executor(None, target, *args)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.remove)

        return task

    def get_system_info(self) -> dict[str, Any]:
        """Return system information."""
        return {
            **self.lic_file.as_dict(),
            "assigned_workstations": len(self.workstations.registered_workstations),
        }

    async def async_verify_app_state(self) -> str | None:
        """Return the current app config data and state."""
        while self.state in [CoreState.starting, CoreState.stopping]:
            await asyncio.sleep(0.5)
        if self.state == CoreState.not_licensed:
            return "license"
        if self.state != CoreState.running:
            raise PConnError(f"App is on {self.state} state")
        return None

    def async_create_task(
        self, target: Coroutine[Any, Any, _R], name: str | None = None
    ) -> asyncio.Task[_R]:
        """Create a task from within the event loop.

        This method must be run in the event loop. If you are using this in your
        integration, use the create task methods on the config entry instead.

        target: target to call.
        """
        task = self.loop.create_task(target, name=name)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.remove)
        return task

    def async_create_background_task(
        self,
        target: Coroutine[Any, Any, _R],
        name: str,
    ) -> asyncio.Task[_R]:
        """Create a task from within the event loop.

        This is a background task which will not block startup and will be
        automatically cancelled on shutdown. If you are using this in your
        integration, use the create task methods on the config entry instead.

        This method must be run in the event loop.
        """
        task = self.loop.create_task(target, name=name)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.remove)
        return task

    async def async_setup(self) -> None:
        """Setup Gallagher Plugins."""
        # pylint: disable-next=import-outside-toplevel
        from .util.logger import async_setup_logger, set_log_levels

        async_setup_logger(self)
        set_log_levels(self.config.log_config)
        await self.async_add_executor_job(self.config.update)

        lic_path = Path(self.config.path(license_file.LICENSE_KEY))
        try:
            await self.async_add_executor_job(
                license_file.validate_license, self, lic_path
            )
        except license_file.LicenseNotFound:
            _LOGGER.info("No license found. Fresh install perhaps")
        except license_file.LicenseNotValid as err:
            _LOGGER.error(str(err))

        # pylint: disable-next=import-outside-toplevel
        from . import interfaces

        await interfaces.async_setup(self)
        self.data[file_upload.DOMAIN] = await self.async_add_executor_job(
            file_upload.FileUploadData.create, self
        )

        await self.async_run()

    async def async_run(self) -> None:
        """Setup gll_plugins app."""
        if self.lic_file is None or not self.lic_file.valid:
            self.state = CoreState.not_licensed
            return
        if self.state == CoreState.running:
            return

        _LOGGER.info("Gallagher Plugins is starting")
        self.state = CoreState.starting

        await self.plugin_entries.async_initialize()
        await self.workstations.async_initialize()

        if domains := self.plugin_entries.async_domains():
            licensed_domains = [
                domain
                for domain in domains
                if domain in self.lic_file.licensed_plugins()
            ]
            # pylint: disable-next=import-outside-toplevel
            from .setup import async_setup_interface

            await asyncio.gather(
                *(async_setup_interface(self, domain) for domain in licensed_domains)
            )
        _LOGGER.info("Gallagher Plugins started")
        self.state = CoreState.running

    async def async_stop(self) -> None:
        """Stop Gallagher Plugins and all plugin entries."""
        if self.state == CoreState.not_running:
            return

        # Cancel all background tasks
        for task in self._background_tasks:
            self._tasks.add(task)
            task.add_done_callback(self._tasks.remove)
            task.cancel("Gallagher Plugins is stopping")

        self.state = CoreState.stopping
        if self._tasks:
            await asyncio.wait([*self._tasks], timeout=10)

        file_uploads: file_upload.FileUploadData = self.data[file_upload.DOMAIN]
        file_uploads.cleanup_unused_files()

        self.state = CoreState.stopped
