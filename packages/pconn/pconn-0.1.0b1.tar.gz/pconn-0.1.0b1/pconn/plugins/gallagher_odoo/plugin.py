"""Odoo plugin class."""

import logging
from typing import Any, TypedDict

from gallagher_restapi import MOVEMENT_EVENT_TYPES, Client, EventFilter, FTEvent
from gallagher_restapi.models import FTPersonalDataFieldDefinition

from pconn.const import SIGNAL_DATA_UPDATED, SIGNAL_STATUS_UPDATED
from pconn.core import PConn
from pconn.plugin_entries import PluginEntry, view
from pconn.plugins import Plugin
from pconn.plugins.gallagher_rest import GallagherREST

from .client import OdooClient
from .const import (
    CONF_GLL_UNIQUE_PDF,
    CONF_ODOO_UNIQUE_FIELD,
    CONF_ONE_READER_DOORS,
    CONF_TWO_READER_DOORS,
    DOMAIN,
)
from .errors import ConfigError, OdooError, RequestError

_LOGGER = logging.getLogger(__name__)


class EventRecord(TypedDict):
    """Event Record object."""

    time: str
    door: str
    direction: str
    name: str
    id: str


class Odoo(Plugin[list[EventRecord]], GallagherREST):
    """Class for interfacing with Odoo system."""

    def __init__(
        self,
        pconn: PConn,
        entry: PluginEntry,
        gll_client: Client,
        odoo_client: OdooClient,
    ) -> None:
        """Initialize plugin."""
        Plugin.__init__(self, pconn, entry, _LOGGER, name=DOMAIN, stream_data=True)
        GallagherREST.__init__(self, pconn, entry, gll_client)
        self.odoo_client = odoo_client
        self.updates_link: str | None = None
        self.doors: dict[str, str] = {}
        self._buffered_events: list[FTEvent] = []
        self.event_records: list[EventRecord] = []

    @property
    def gll_unique_pdf(self) -> str:
        """Return the unique_field for identifying cardholders in Gallagher."""
        return self.plugin_entry.options[CONF_GLL_UNIQUE_PDF]

    @property
    def odoo_unique_field(self) -> str:
        """Return the unique_field for identifying cardholders in Odoo."""
        return self.plugin_entry.options[CONF_ODOO_UNIQUE_FIELD]

    @property
    def two_readers_door_ids(self) -> list[str]:
        """Return the ids of doors having two readers."""
        return self.plugin_entry.options.get(CONF_TWO_READER_DOORS, [])

    @property
    def one_reader_door_ids(self) -> list[str]:
        """Return the ids of doors having one reader."""
        return self.plugin_entry.options.get(CONF_ONE_READER_DOORS, [])

    @property
    def monitored_doors(self) -> list[str]:
        """Return list of gallagher event sources."""
        return self.one_reader_door_ids + self.two_readers_door_ids

    @property
    def gll_event_filter(self) -> EventFilter:
        """Return Gallagher client event filter."""
        return EventFilter(
            event_types=MOVEMENT_EVENT_TYPES,
            fields=["defaults", "eventType", f"cardholder.pdf_{self.gll_unique_pdf}"],
            sources=self.monitored_doors,
            previous=True,
            top=1,
        )

    @property
    def can_sync(self) -> bool:
        """Return if plugin can run in background."""
        return all(
            key in self.plugin_entry.options
            for key in ("gll_unique_pdf", "odoo_unique_field")
        ) and bool(self.monitored_doors)

    @property
    def available(self) -> bool:
        """Return if plugin is available."""
        return self.odoo_client.connected

    async def async_get_gll_unique_fields(self) -> list[FTPersonalDataFieldDefinition]:
        """Return list of unique personal fields."""
        pdfs = await self.gll_client.get_personal_data_field(
            extra_fields=["defaults", "unique"]
        )
        return [pdf for pdf in pdfs if pdf.unique]

    async def async_get_odoo_unique_fields(self) -> dict[str, str]:
        """Return list of unique personal fields."""
        return await self.pconn.async_add_executor_job(
            self.odoo_client.get_employee_fields
        )

    async def async_get_doors(self) -> dict[str, str]:
        """Return list of available doors."""
        doors = await self.gll_client.get_door(extra_fields=["id", "name"])
        self.doors = {door.id: door.name for door in doors}
        return self.doors

    @view
    def get_data(self) -> dict[str, Any]:
        """Return plugin status."""
        return {
            "odoo_connection": self.odoo_client.connected,
            "odoo_host": self.odoo_client.host,
            "monitored_doors": [
                self.doors[door_id] for door_id in self.monitored_doors
            ],
            "event_records": self.event_records,
        }

    async def async_initialize(self) -> None:
        """Initialize the plugin."""
        if not await self.async_get_doors():
            raise ConfigError("At least one Gallagher door is required.")
        if not await self.async_get_gll_unique_fields():
            raise ConfigError("At least one Gallagher unique field is required.")
        if not await self.async_get_odoo_unique_fields():
            raise ConfigError("At least one Odoo employee field is required.")

        if self.can_sync:
            self.plugin_entry.async_on_unload(
                self.listen_for_events(self.gll_event_filter, self.async_handle_event)
            )

    async def async_handle_event(self, events: list[FTEvent]) -> None:
        """Initialize listener."""
        if not events:
            return
        self._buffered_events += events

        if not self.odoo_client.connected:
            try:
                await self.pconn.async_add_executor_job(self.odoo_client.connect)
            except OdooError:
                await self.event_queue.put(
                    (
                        SIGNAL_STATUS_UPDATED,
                        {"odoo_connection": self.odoo_client.connected},
                    )
                )
                return
        try:
            await self.pconn.async_add_executor_job(self.push_events_to_odoo)
        except OdooError as err:
            _LOGGER.error("Odoo Error: %s", err)
        else:
            await self.event_queue.put((SIGNAL_DATA_UPDATED, self.event_records))
            self._buffered_events = []
        await self.event_queue.put(
            (SIGNAL_STATUS_UPDATED, {"odoo_connection": self.odoo_client.connected})
        )

    def push_events_to_odoo(self) -> None:
        """Push events to Odoo server."""
        for event in self._buffered_events:
            if not event.cardholder or not (
                cardholder_id := list(event.cardholder.pdfs.values())
            ):
                _LOGGER.warning(
                    "No Cardholder found in the event "
                    "or the unique pdf field is not assigned."
                )
                continue
            try:
                if not (
                    odoo_employee_id := self.odoo_client.get_employee_id(
                        self.odoo_unique_field, str(cardholder_id[0])
                    )
                ):
                    _LOGGER.warning(
                        "Employee with id %s is not found in Odoo server.",
                        cardholder_id[0],
                    )
                    continue

                consider_entry = True
                # 20003 is the only exit event type,
                # other types are considered as entry
                if event.eventType and event.eventType.id != "20003":
                    if not hasattr(event, "source"):
                        _LOGGER.debug(
                            "Event source is unknown. Assuming its an entry event."
                        )
                    elif event.source.id in self.one_reader_door_ids:
                        consider_entry = False
                else:
                    consider_entry = False

                if not consider_entry:
                    last_attendance = self.odoo_client.get_last_attendance(
                        odoo_employee_id
                    )
                    if last_attendance and not last_attendance["check_out"]:
                        self.odoo_client.add_checkout(last_attendance["id"], event.time)
                        _LOGGER.info(
                            "Exit event registered for %s through %s at %s",
                            event.cardholder.name,
                            event.source.name,
                            event.time.astimezone().isoformat(),
                        )
                        self.event_records.append(
                            {
                                "time": event.time.astimezone().isoformat(),
                                "door": event.source.name,
                                "direction": "OUT",
                                "name": event.cardholder.name,
                                "id": str(cardholder_id[0]),
                            }
                        )
                        continue
                # create a new attendance
                self.odoo_client.create_attendance(odoo_employee_id, event.time)
                _LOGGER.info(
                    "Entry event registered for %s through %s at %s",
                    event.cardholder.name,
                    event.source.name,
                    event.time.strftime("%H:%M:%S"),
                )
                self.event_records.append(
                    {
                        "time": event.time.astimezone().isoformat(),
                        "door": event.source.name,
                        "direction": "IN",
                        "name": event.cardholder.name,
                        "id": str(cardholder_id[0]),
                    }
                )
            except RequestError as err:
                _LOGGER.error(
                    "Error pushing event for %s at %s: %s",
                    event.cardholder.name,
                    event.time.astimezone().isoformat(),
                    str(err),
                )
                continue
