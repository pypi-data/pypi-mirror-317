"""Demo plugin."""

from collections.abc import Callable
from datetime import date, datetime, time
from enum import StrEnum
import logging
from typing import Any, TypedDict

from gallagher_restapi import MOVEMENT_EVENT_TYPES, Client
from gallagher_restapi.exceptions import GllApiError
from gallagher_restapi.models import EventFilter, FTItemStatus
from google.api_core.exceptions import DeadlineExceeded
from google.generativeai import GenerativeModel

from pconn.const import SIGNAL_DATA_UPDATED
from pconn.core import PConn
from pconn.exceptions import PluginActionError
from pconn.plugin_entries import PluginEntry, view
from pconn.plugins import Plugin
from pconn.plugins.ai_analyzer import AIAnalyzer
from pconn.plugins.gallagher_rest import GallagherREST

from .const import CONF_DATA_TYPES, DOMAIN, ITEM_TYPES, DataType

_LOGGER = logging.getLogger(__name__)

DATA_TYPES: dict[StrEnum, Callable[..., Any]] = {
    DataType.ALARMS: lambda analyzer: analyzer.async_get_alarms,
    DataType.CARDHOLDERS: lambda analyzer: analyzer.async_get_cardholders,
    DataType.CARDHOLDER_EVENTS: lambda analyzer: analyzer.async_get_card_events,
    DataType.CONTROLLERS: lambda analyzer: analyzer.async_get_controllers,
    DataType.DOORS: lambda analyzer: analyzer.async_get_doors,
    DataType.READERS: lambda analyzer: analyzer.async_get_readers,
}


class ChatHistory(TypedDict):
    """Chat history dictionary."""

    type: DataType
    question: str
    answer: str


class GallagherAIAnalyzer(Plugin, GallagherREST, AIAnalyzer):
    """Gallagher AI Analyzer plugin class."""

    def __init__(
        self,
        pconn: PConn,
        entry: PluginEntry,
        gll_client: Client,
        ai_model: GenerativeModel,
    ) -> None:
        """Initialize plugin."""
        Plugin.__init__(self, pconn, entry, _LOGGER, name=DOMAIN, stream_data=True)
        GallagherREST.__init__(self, pconn, entry, gll_client)
        AIAnalyzer.__init__(self, pconn, entry, ai_model)
        self.chat_history: list[ChatHistory] = []

    @property
    def exposed_data_types(self) -> list[str]:
        """Return list of exposed types of data."""
        return self.plugin_entry.options.get(CONF_DATA_TYPES, [])

    @view
    async def get_chat_history(self) -> list[ChatHistory]:
        """Return chat history."""
        return self.chat_history

    @view
    async def ask_question(self, question: str) -> bool:
        """Get the question and stream the response."""
        self.pconn.async_create_task(self._analyze_question(question))
        return True

    async def _analyze_question(self, question: str) -> None:
        """Analyze the question based on the item type data and return response."""
        data_type = DataType.NONE
        answer = ""
        try:
            data_type = await self.async_analyze_question(question, DataType)
            if (
                self.chat_history
                and (previous_data_type := self.chat_history[-1]["type"])
                and data_type in [previous_data_type, DataType.NONE]
            ):
                if await self.verify_followup_question(question):
                    response = await self.async_generate_followup_response(question)
                    async for chunk in response:
                        answer += chunk
                        await self.event_queue.put((SIGNAL_DATA_UPDATED, chunk))
                else:
                    answer = "Please refine your question."
                    await self.event_queue.put((SIGNAL_DATA_UPDATED, answer))
            else:
                if data_type not in self.exposed_data_types:
                    if data_type != DataType.NONE:
                        answer = f"Are you asking about **{data_type}**.\n This type is not exposed to the AI."
                    else:
                        answer = "Please refine your question."
                    await self.event_queue.put((SIGNAL_DATA_UPDATED, answer))
                else:
                    try:
                        data = await DATA_TYPES[data_type](self)()
                    except GllApiError as err:
                        raise PluginActionError(err)

                    response = await self.async_generate_response(question, data)
                    async for chunk in response:
                        answer += chunk
                        await self.event_queue.put((SIGNAL_DATA_UPDATED, chunk))
        except DeadlineExceeded:
            answer = "Timed out while waiting for answer."
            await self.event_queue.put((SIGNAL_DATA_UPDATED, answer))
        finally:
            chat = ChatHistory(type=data_type, question=question, answer=answer)
            _LOGGER.debug(chat)
            self.chat_history.append(chat)
            await self.event_queue.put((SIGNAL_DATA_UPDATED, "finished"))

    async def _get_items_status(self, item_ids: list[str]) -> list[FTItemStatus]:
        """Return list of item status."""
        await self.gll_client.get_item_status(item_ids)
        # ignore the first call as the status might be unknown
        items_status, _ = await self.gll_client.get_item_status(item_ids)
        return items_status

    async def _async_get_items(self, item_type: DataType) -> dict[str, Any]:
        """Return list of items."""
        if not (item_types := ITEM_TYPES.get(item_type)):
            raise PluginActionError("Unknown item type")
        items = await self.gll_client.get_item(
            item_types=item_types, extra_fields=["connectedController"]
        )

        items_status = await self._get_items_status([item.id for item in items])

        return {
            item_type: [
                {
                    "name": item.name,
                    "status": _get_item_status(item.id, items_status),
                    "connected_controller": item.extra_fields.get(
                        "connectedController"
                    ),
                }
                for item in items
            ]
        }

    async def async_get_cardholders(self) -> list[dict[str, Any]]:
        """Return list of cardholder data."""

        cardholders = await self.gll_client.get_cardholder(
            extra_fields=["cards", "personalDataFields", "lastSuccessfulAccessZone"]
        )
        return [
            {
                "name": f"{cardholder.firstName} {cardholder.lastName}",
                "description": cardholder.description,
                "notes": cardholder.notes,
                "authorized": cardholder.authorised,
                "current location": cardholder.lastSuccessfulAccessZone.name
                if cardholder.lastSuccessfulAccessZone
                else None,
                "personal fields": {
                    key: value
                    for key, value in cardholder.pdfs.items()
                    if isinstance(value, (str, int))
                },
                "cards": [
                    {
                        "number": card.number,
                        "type": card.type.name,
                        "status": card.status.value,
                    }
                    for card in cardholder.cards or []
                ],
            }
            for cardholder in cardholders
        ]

    async def async_get_doors(self) -> dict[str, Any]:
        """Return list of controller data."""
        doors = await self.gll_client.get_door(
            extra_fields=["connectedController"],
        )
        door_ids = [door.id for door in doors]
        doors_status = await self._get_items_status(door_ids)

        return {
            "doors": [
                {
                    "name": door.name,
                    "description": door.description,
                    "status": _get_item_status(door.id, doors_status),
                    "connected_controller": door.connectedController.name
                    if door.connectedController
                    else None,
                }
                for door in doors
            ],
            "door normal flags": ["closed", "locked", "free"],
            "door alarm flags": ["open too long", "Forced", "offline"],
        }

    async def async_get_readers(self) -> dict[str, Any]:
        """Return list of reader data."""
        return await self._async_get_items(DataType.READERS)

    async def async_get_controllers(self) -> dict[str, Any]:
        """Return list of door data."""
        return await self._async_get_items(DataType.CONTROLLERS)

    async def async_get_alarms(self) -> dict[str, Any]:
        """Return list of alarm data."""
        alarms = await self.gll_client.get_alarms(extra_fields=["eventType"])

        return {
            "alarms": [
                {
                    "active": alarm.active,
                    "priority": alarm.priority,
                    "state": alarm.state,
                    "message": alarm.message,
                    "time": alarm.time.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
                    "source": alarm.source.name,
                    "type": alarm.eventType.name,
                }
                for alarm in alarms
            ]
        }

    async def async_get_events(self, event_filter: EventFilter) -> list[dict[str, Any]]:
        """Return list of events."""

        events = await self.gll_client.get_events(event_filter=event_filter)

        return [
            {
                "message": event.message,
                "time": event.time.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
                "source": event.source.name,
                "type": event.eventType.name,
                "priority": event.priority,
            }
            for event in events
        ]

    async def async_get_card_events(self) -> dict[str, Any]:
        """Return list of card event data."""
        event_filter = EventFilter(
            after=datetime.combine(date.today(), time(0, 0)),
            event_types=MOVEMENT_EVENT_TYPES,
            fields=["defaults", "eventType"],
        )
        events = await self.async_get_events(event_filter=event_filter)

        cardholders = await self.async_get_cardholders()

        return {"entry and exist event": events, "cardholders": cardholders}


def _get_item_status(item_id: str, items_status: list[FTItemStatus]) -> str | None:
    """Get item status."""
    for item_status in items_status:
        if item_status.id == item_id:
            return item_status.statusFlags or item_status.status
    return None
