"""Listen to status updates of Gallagher items."""

import asyncio
from collections.abc import Callable, Coroutine
import logging
from typing import Any

from gallagher_restapi import Client, FTEvent
from gallagher_restapi.exceptions import GllApiError
from gallagher_restapi.models import EventFilter, FTItemReference

from pconn.core import PConn


class UpdateListener:
    """Update Listener for Gallagher items."""

    COOLDOWN = 10

    def __init__(
        self,
        pconn: PConn,
        gll_client: Client,
        logger: logging.Logger,
        update_callback: Callable[
            [list[FTItemReference] | list[FTEvent]], Coroutine[Any, Any, None] | None
        ],
    ) -> None:
        """Initialize the listener."""
        self.pconn = pconn
        self.gll_client = gll_client
        self.logger = logger
        self.stopped = False
        self.update_link: FTItemReference | None = None
        self.update_callback = update_callback

        self.failed_attempts = 0

    async def listen_for_status_updates(self, items: list[str]) -> None:
        """Update items status."""
        while not self.stopped:
            try:
                if self.update_link is not None:
                    (
                        items_status,
                        self.update_link,
                    ) = await self.gll_client.get_item_status(
                        next_link=self.update_link
                    )
                else:
                    (
                        items_status,
                        self.update_link,
                    ) = await self.gll_client.get_item_status(item_ids=items)
            except GllApiError as ex:
                self.update_link = None
                self.logger.error("Error updating items status: %s", ex)
                self.failed_attempts += 1
                if self.failed_attempts > 2:
                    await asyncio.sleep(self.COOLDOWN)
            else:
                if job := self.update_callback(items_status):
                    self.pconn.async_create_task(job)
                self.failed_attempts = 0

    async def listen_for_events(self, event_filter: EventFilter) -> None:
        """Listen for events."""
        while not self.stopped:
            try:
                async for events in self.gll_client.yield_new_events(
                    event_filter=event_filter
                ):
                    if job := self.update_callback(events):
                        self.pconn.async_create_task(job)
                    self.failed_attempts = 0
            except GllApiError as ex:
                self.logger.error("Error updating items status: %s", ex)
                self.failed_attempts += 1
                if self.failed_attempts > 3:
                    await asyncio.sleep(self.COOLDOWN)
