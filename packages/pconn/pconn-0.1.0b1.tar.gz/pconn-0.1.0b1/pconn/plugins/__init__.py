"""Plugins for interfacing with Gallagher Command using REST api."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
import contextlib
from datetime import timedelta
import logging
from random import randint
from typing import TYPE_CHECKING, Any, Generic

import httpx
from typing_extensions import TypeVar

from pconn.const import SIGNAL_DATA_UPDATED
from pconn.core import CALLBACK_TYPE, PConn
from pconn.helpers import format_stream_message

if TYPE_CHECKING:
    from pconn.plugin_entries import PluginEntry

RANDOM_MICROSECOND_MIN = 50000
RANDOM_MICROSECOND_MAX = 500000

_DataT = TypeVar("_DataT", default=dict[str, Any])


class UpdateFailed(Exception):
    """Raised when an update has failed."""


class Plugin(Generic[_DataT]):
    """Base class for plugins."""

    def __init__(
        self,
        pconn: PConn,
        plugin_entry: PluginEntry,
        logger: logging.Logger,
        *,
        name: str,
        update_interval: timedelta | None = None,
        stream_data: bool = False,
    ) -> None:
        """Initialize plugin."""
        self.pconn = pconn
        self.plugin_entry = plugin_entry
        self.logger = logger
        self.name = name
        self.httpx_client = httpx.AsyncClient(
            verify=False
        )  # implement certificate per plugin?

        self._unsub_refresh: CALLBACK_TYPE | None = None

        self._microsecond = (
            randint(RANDOM_MICROSECOND_MIN, RANDOM_MICROSECOND_MAX) / 10**6
        )
        self.last_update_success = True
        self.update_interval = update_interval
        self.log_failures = True
        self._shutdown_requested = False
        self.plugin_entry.async_on_unload(self.async_shutdown)
        self.data: _DataT = None  # type: ignore[assignment]
        self.event_queue: asyncio.Queue[tuple[str, Any]] = asyncio.Queue()
        if stream_data:
            self.plugin_entry.add_event_stream(self.dispatch_updated_data)

    async def async_shutdown(self) -> None:
        """Cancel any scheduled call, and ignore new runs."""
        self._shutdown_requested = True
        self._async_unsub_refresh()

    async def _async_update_data(self) -> _DataT:
        """Fetch the latest data from the source."""
        raise NotImplementedError("Update method not implemented")

    def _async_unsub_refresh(self) -> None:
        """Cancel any scheduled call."""
        if self._unsub_refresh:
            self._unsub_refresh()
            self._unsub_refresh = None

    def _schedule_refresh(self) -> None:
        """Schedule a refresh."""
        if self.update_interval is None:
            return

        self._async_unsub_refresh()

        now = self.pconn.loop.time()

        next_refresh = int(now) + self._microsecond
        next_refresh += self.update_interval.total_seconds()
        self._unsub_refresh = self.pconn.loop.call_at(
            next_refresh, lambda: asyncio.ensure_future(self.async_refresh())
        ).cancel

    async def async_refresh(self) -> None:
        """Refresh data."""
        self._async_unsub_refresh()
        if self._shutdown_requested:
            return
        previous_data = self.data
        try:
            self.data = await self._async_update_data()
        except TimeoutError:
            if self.last_update_success:
                self.logger.error("Timeout fetching %s data", self.name)
                self.last_update_success = False
        except UpdateFailed as err:
            if self.last_update_success:
                self.logger.error("Error updating %s data: %s", self.name, err)
                self.last_update_success = False

        except Exception as err:  # pylint: disable=broad-except
            self.last_update_success = False
            self.logger.exception(
                "Unexpected error updating %s data: %s", self.name, err
            )
        else:
            if not self.last_update_success:
                self.last_update_success = True
                self.log_failures = True
                self.logger.info("Fetching %s data recovered", self.name)
        finally:
            self.logger.debug("Finished updating data for %s", self.name)
            self._schedule_refresh()

        if self.last_update_success and previous_data != self.data:
            await self.event_queue.put((SIGNAL_DATA_UPDATED, self.data))

    async def dispatch_updated_data(self) -> AsyncGenerator[str, None]:
        """Dispatch updated data."""
        while not self._shutdown_requested:
            with contextlib.suppress(TimeoutError):
                event, data = await asyncio.wait_for(self.event_queue.get(), timeout=10)
                yield format_stream_message(event, data)
                self.event_queue.task_done()
