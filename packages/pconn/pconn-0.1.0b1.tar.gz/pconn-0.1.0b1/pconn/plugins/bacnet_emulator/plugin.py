"""BACnet Emulator plugin."""

import logging
from pathlib import Path
from typing import Any, cast

import BAC0
from bacpypes.basetypes import BinaryPV

from pconn.core import PConn
from pconn.plugin_entries import PluginEntry, view
from pconn.util.json import json_loads, save_json

from .bacnet_device import BACnetDevice
from .bacnet_objects import ObjectBase
from .const import CONF_DISABLED_ITEMS, CONF_NEW_ID, CONF_REGISTERED_ITEMS

_LOGGER = logging.getLogger(__name__)

BACNET_POINTS = ".bacnet_points"


class BACnetEmulator:
    """BACnet emulator for Gallagher items."""

    items: dict[str, ObjectBase]

    def __init__(
        self,
        pconn: PConn,
        entry: PluginEntry,
        device: BAC0.lite,
    ) -> None:
        """Initialize the emulator."""
        self.pconn = pconn
        self.plugin_entry = entry
        self.device = BACnetDevice(device, self._value_updated_cb)
        self.items = {}
        self._registered_items: dict[str, dict[str, list[tuple[int, str | None]]]] = {}
        self._disabled_items: list[str] = []
        self.commendable_items: dict[int, ObjectBase] = {}
        self._new_id = 0
        self._load_registered_items()

    @property
    def device_id(self) -> str:
        """Return BACnet device ID."""
        return self.device.device.this_application.localDevice.objectIdentifier[1]

    @property
    def registered_items_ids(self) -> list[str]:
        """Return list of registered item ids."""
        return [key for d in self._registered_items.values() for key in d]

    def _load_registered_items(self) -> None:
        """Load registered items from file."""
        bacnet_points_path = Path(self.pconn.config.path(BACNET_POINTS))
        if bacnet_points_path.exists():
            config = cast(
                dict[str, Any],
                json_loads(bacnet_points_path.read_text(encoding="utf-8")),
            )
            self._new_id = config[CONF_NEW_ID]
            self._registered_items = config[CONF_REGISTERED_ITEMS]
            self._disabled_items = config[CONF_DISABLED_ITEMS]

    def _save_to_file(self) -> None:
        """Save registered items to file."""
        bacnet_points_path = self.pconn.config.path(BACNET_POINTS)
        _dict = {
            CONF_NEW_ID: self._new_id,
            CONF_REGISTERED_ITEMS: self._registered_items,
            CONF_DISABLED_ITEMS: self._disabled_items,
        }
        save_json(bacnet_points_path, _dict)

    @view
    async def disable_item(self, item_id: str, disabled: bool) -> None:
        """Disable an item."""
        if item_id not in self.registered_items_ids:
            return

        if _object := self.items.get(item_id):
            _object.disabled = disabled
            _object.update_object_value()
        if disabled and item_id not in self._disabled_items:
            self._disabled_items.append(item_id)
        else:
            self._disabled_items.remove(item_id)
        _LOGGER.debug("Gallagher item %s disabled: %s", item_id, disabled)
        await self.pconn.async_add_executor_job(self._save_to_file)

    def _get_objects(self) -> list[dict[str, Any]]:
        """Return the list of objects info."""
        objects: list[dict[str, Any]] = []
        for item in self.items.values():
            objects += item.objects_info()
        objects.sort(key=lambda x: x["name"])
        return objects

    @view
    def get_data(self) -> dict[str, Any]:
        """Return plugin info."""
        return {"id": self.device_id, "objects": self._get_objects()}

    def _value_updated_cb(self, object_id: int, new_value: BinaryPV) -> None:
        """Update the value of the item."""
        _LOGGER.debug("Object %s value updated to %s externally", object_id, new_value)
        if item := self.commendable_items.get(object_id):
            self.plugin_entry.async_create_task(
                self.pconn, item.object_updated_cb(new_value)
            )
