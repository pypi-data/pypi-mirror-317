"""Represent each exposed item as a BACnet object."""

from pydoc import describe
from typing import Any, TypeVar

from bacpypes.basetypes import BinaryPV, Reliability
from gallagher_restapi import Client
from gallagher_restapi.models import FTDoor, FTInput, FTItem, FTOutput

from pconn.plugins.bacnet_emulator.bacnet_device import OBJECT_TYPES, BACnetDevice
from pconn.plugins.bacnet_emulator.plugin import ObjectBase
from pconn.plugins.gallagher_rest.const import UNAVAILABLE_FLAGS

_ITEM_TYPES = TypeVar("_ITEM_TYPES", FTDoor, FTInput, FTOutput, FTItem)


class GallagherObject(ObjectBase):
    """Base class for BACnet objects."""

    def __init__(
        self,
        item: _ITEM_TYPES,
        bacnet_device: BACnetDevice,
        *,
        disabled: bool = False,
        gll_client: Client | None = None,
    ) -> None:
        """Initialize the object."""
        self.item = item
        self.gll_client = gll_client
        super().__init__(item.name, bacnet_device, disabled=disabled)

    @property
    def out_of_service(self) -> bool:
        """Return True if parent device is offline."""
        return self.disabled or any(
            flag in UNAVAILABLE_FLAGS for flag in self.status_flags
        )

    @property
    def status_flags(self) -> list[str]:
        """Return the statusFlags of the object."""
        if self._status_flags:
            return self._status_flags
        if status_flags := getattr(self.item, "statusFlags", None):
            self._status_flags = status_flags
        elif isinstance(self.item, FTItem) and "statusFlags" in self.item.extra_fields:
            self._status_flags = self.item.extra_fields["statusFlags"]
        return self._status_flags

    def objects_info(self) -> list[dict[str, Any]]:
        """Return the list of objects info."""
        _data: list[dict[str, Any]] = []
        for _object in self.objects:
            _data.append(
                {
                    "name": _object.objectName,
                    "identifier": _object.objectIdentifier,
                    "ftItemId": self.item.id,
                    "presentValue": _object.presentValue.value,
                    "disabled": self.disabled,
                    "outOfService": _object.outOfService,
                    "flags": self.status_flags,
                }
            )
        return _data

    def update_object_value(self, new_status_flags: list[str] | None = None) -> None:
        """Update the value of the object."""
        if new_status_flags is not None:
            self._status_flags = new_status_flags
        super().update_object_value()


class GallagherControllerObject(GallagherObject):
    """Represent a controller point as a BACnet object."""

    @property
    def health_value(self) -> int:
        """Return the health value of the controller."""
        return 1 if self.out_of_service else 0

    @property
    def tamper_value(self) -> int:
        """Return the tamper status of the controller."""
        return 1 if "tamper" in self.status_flags else 0

    @property
    def out_of_service(self) -> bool:
        """Controller is out of service if unconfigured."""
        return self.disabled or "unconfigured" in self.status_flags

    def add_object_to_device(self, object_id: int, suffix: str | None = None) -> None:
        """Add the object to the BACnet device."""
        name = self.item.name
        if suffix:
            name += f" - {suffix}"
        initial_value = self.health_value if suffix == "Health" else self.tamper_value
        bacnet_object = self.bacnet.add_object(
            self.object_type, instance=object_id, name=name, initial_value=initial_value
        )
        self.objects += bacnet_object

    def update_object_value(self, new_status_flags: list[str] | None = None) -> None:
        """Update the value of the object."""
        if new_status_flags is not None:
            self._status_flags = new_status_flags
        for bacnet_object in self.objects:
            bacnet_object.outOfService = self.out_of_service
            if not self.out_of_service:
                if "Health" in bacnet_object.objectName:
                    bacnet_object.presentValue = BinaryPV(self.health_value)
                elif "Tamper" in bacnet_object.objectName:
                    bacnet_object.presentValue = BinaryPV(self.tamper_value)
                self.bacnet.objects_values[bacnet_object.objectIdentifier[1]] = (
                    bacnet_object.presentValue
                )


class GallagherIOBaseObject(GallagherObject):
    """Represent an input/output point as a BACnet object."""

    @property
    def present_value(self) -> int:
        """Return the presentValue of the object."""
        return 0 if "open" in self.status_flags else 1


class GallagherInputObject(GallagherIOBaseObject):
    """Represent an input point as a BACnet object."""

    @property
    def tamper_value(self) -> int:
        """Return the tamper status of input item."""
        return 4 if "tamper" in self.status_flags else 0

    def update_object_value(self, new_status_flags: list[str] | None = None) -> None:
        """Update the value of the input object."""
        super().update_object_value(new_status_flags)
        for _object in self.objects:
            _object.reliability = Reliability(self.tamper_value)


class GallagherOutputObject(GallagherIOBaseObject):
    """Represent an output point as a BACnet object."""

    @property
    def object_type(self) -> OBJECT_TYPES:
        """Return the presentValue of the object."""
        return OBJECT_TYPES.BINARY_OUTPUT

    async def object_updated_cb(self, new_value: BinaryPV) -> None:
        """Update output in Gallagher server."""
        if self.gll_client is None:
            return
        if self.item.commands is None:
            if item := await self.gll_client.get_output(id=self.item.id):
                self.item = item[0]
            else:
                return
        assert self.item.commands is not None
        command = (
            self.item.commands.on
            if new_value.value == "active"
            else self.item.commands.off
        )
        await self.gll_client.override_output(command)
