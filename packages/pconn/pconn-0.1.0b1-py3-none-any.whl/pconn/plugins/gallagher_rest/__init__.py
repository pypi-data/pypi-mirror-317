"""Demo plugin to show functionalities."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
import logging
from typing import Any, Literal

from gallagher_restapi.client import Client, CloudGateway
from gallagher_restapi.exceptions import GllApiError
from gallagher_restapi.models import (
    EventFilter,
    FTEvent,
    FTItemReference,
    FTPersonalDataFieldDefinition,
)

from pconn.core import PConn
from pconn.exceptions import PluginEntryError
from pconn.helpers.httpx_client import create_async_httpx_client
from pconn.plugin_entries import PluginEntry

from .listeners import UpdateListener

DOMAIN = "gallagher_rest"


async def async_setup_entry(pconn: PConn, entry: PluginEntry[Client]) -> bool:
    """Setup demo plugin from config."""
    gll_client = get_gll_client(pconn, **entry.data)
    try:
        await gll_client.initialize()
    except GllApiError as err:
        raise PluginEntryError(str(err)) from err

    entry.plugin_data = gll_client
    return True


def get_gll_client(
    pconn: PConn,
    *,
    api_key: str,
    cloud_gateway: Literal["AU_GATEWAY", "US_GATEWAY"] | None = None,
    host: str | None = None,
    port: int | None = None,
    token: str | None = None,
    use_ssl: bool = False,
) -> Client:
    """Return an instance of Gallagher rest api client."""
    params: dict[str, Any] = {"api_key": api_key}
    if token:
        params["token"] = token
    if cloud_gateway:
        params["cloud_gateway"] = CloudGateway[cloud_gateway]
    elif host is None or port is None:
        raise ValueError("Host and port must be provided")
    else:
        params.update({"host": host, "port": port})

    return Client(**params, httpx_client=create_async_httpx_client(pconn, use_ssl))


class GallagherREST:
    """Demo plugin class."""

    def __init__(self, pconn: PConn, entry: PluginEntry, gll_client: Client) -> None:
        """Initialize plugin."""
        self.pconn = pconn
        self.plugin_entry = entry
        self.gll_client = gll_client

    def listen_for_updates(
        self,
        items: list[str],
        update_callback: Callable[
            [list[FTItemReference]], Coroutine[Any, Any, None] | None
        ],
    ) -> Callable[[], None]:
        """Listen for updates."""

        def unsub() -> None:
            """Unsubscribe from updates."""
            update_listener.stopped = True

        update_listener = UpdateListener(
            self.pconn,
            self.gll_client,
            logging.getLogger(self.plugin_entry.domain),
            update_callback,
        )
        self.plugin_entry.async_create_background_task(
            self.pconn,
            update_listener.listen_for_status_updates(items),
            f"{self.plugin_entry.domain}-{self.plugin_entry.entry_id}-updates-listener",
        )

        return unsub

    def listen_for_events(
        self,
        event_filter: EventFilter,
        update_callback: Callable[[list[FTEvent]], Coroutine[Any, Any, None] | None],
    ) -> Callable[[], None]:
        """Listen for updates."""

        def unsub() -> None:
            """Unsubscribe from updates."""
            update_listener.stopped = True

        update_listener = UpdateListener(
            self.pconn,
            self.gll_client,
            logging.getLogger(self.plugin_entry.domain),
            update_callback,
        )
        self.plugin_entry.async_create_background_task(
            self.pconn,
            update_listener.listen_for_events(event_filter),
            f"{self.plugin_entry.domain}-{self.plugin_entry.entry_id}-event-listener",
        )

        return unsub

    async def async_get_unique_fields(self) -> list[FTPersonalDataFieldDefinition]:
        """Return list of unique personal fields."""
        pdfs = await self.gll_client.get_personal_data_field(
            extra_fields=["defaults", "unique"]
        )
        return [pdf for pdf in pdfs if pdf.unique]
