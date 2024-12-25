"""Represent each exposed item as a BACnet object."""

from typing import Any

from bacpypes.basetypes import BinaryPV
from bacpypes.local.object import Object

from .bacnet_device import OBJECT_TYPES, BACnetDevice


class ObjectBase:
    """Base class for BACnet objects."""

    def __init__(
        self,
        name: str,
        bacnet: BACnetDevice,
        *,
        disabled: bool = False,
    ) -> None:
        """Initialize the object."""
        self.name = name
        self.bacnet = bacnet
        self.objects: list[Object] = []
        self._status_flags: list[str] = []
        self.disabled = disabled

    @property
    def present_value(self) -> int:
        """Return the presentValue of the object."""
        raise NotImplementedError

    @property
    def tamper_value(self) -> int:
        """Return the tamper value of the object."""
        raise NotImplementedError

    @property
    def out_of_service(self) -> bool:
        """Return True if parent device is offline."""
        return self.disabled

    @property
    def object_type(self) -> OBJECT_TYPES:
        """Return the object type of the object."""
        return OBJECT_TYPES.BINARY_INPUT

    def objects_info(self) -> list[dict[str, Any]]:
        """Return the list of objects info."""
        _data: list[dict[str, Any]] = []
        for _object in self.objects:
            _data.append(
                {
                    "name": _object.objectName,
                    "identifier": _object.objectIdentifier,
                    "presentValue": _object.presentValue.value,
                    "disabled": self.disabled,
                    "outOfService": _object.outOfService,
                }
            )
        return _data

    def add_object_to_device(self, object_id: int, suffix: str | None = None) -> None:
        """Add the object to the BACnet device."""
        name = self.name
        if suffix:
            name += f" - {suffix}"
        bacnet_object = self.bacnet.add_object(
            self.object_type,
            instance=object_id,
            name=name,
            initial_value=self.present_value,
        )
        self.objects += bacnet_object

    def update_object_value(self) -> None:
        """Update the value of the object."""
        for bacnet_object in self.objects:
            if self.out_of_service:
                bacnet_object.outOfService = True
                continue
            bacnet_object.outOfService = False
            bacnet_object.presentValue = BinaryPV(self.present_value)
            self.bacnet.objects_values[bacnet_object.objectIdentifier[1]] = (
                bacnet_object.presentValue
            )

    async def object_updated_cb(self, new_value: BinaryPV) -> None:
        """Callback function if bacnet object is updated externally."""
