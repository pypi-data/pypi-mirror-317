"""BACnet device emulator for Gallagher items."""

from collections.abc import Callable
from enum import Enum
import logging
import threading
from time import sleep
from typing import Any

import BAC0
from BAC0.core.devices.local.models import binary_input, binary_output
from BAC0.core.devices.local.object import ObjectFactory
from bacpypes.basetypes import BinaryPV
from bacpypes.local.object import Object
from bacpypes.primitivedata import Boolean

from .const import DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)


class OBJECT_TYPES(Enum):
    """Enumerate object types."""

    BINARY_INPUT = binary_input
    BINARY_OUTPUT = binary_output

    def __call__(self, **kwargs: Any) -> ObjectFactory:
        """Call the function associated with the object type."""
        return self.value(kwargs)


def create_device(
    *, ip: str, deviceId: int, port: int | None = None, bbmdAddress: str | None = None
) -> BAC0.lite:
    """Create a BACnet device."""
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("BAC0"):
            logging.getLogger(logger_name).setLevel(logging.ERROR)
    return BAC0.lite(
        ip=ip,
        port=port or DEFAULT_PORT,
        mask=24,
        deviceId=deviceId,
        bbmdAddress=bbmdAddress,
        bbmdTTL=600 if bbmdAddress else 0,
    )


class BACnetDevice(threading.Thread):
    """BACnet emulator for Gallagher items."""

    def __init__(
        self,
        device: BAC0.lite,
        value_updated_cb: Callable[[int, BinaryPV], None],
    ) -> None:
        """Initialize the emulator."""
        threading.Thread.__init__(self, name="bacnet_emulator", daemon=True)
        self.device = device
        self.stopped = False
        self.objects_values: dict[int, BinaryPV] = {}
        self.value_updated_cb = value_updated_cb

    def add_object(
        self,
        object_type: OBJECT_TYPES,
        *,
        instance: int,
        name: str,
        description: str | None = None,
        initial_value: int = 0,
        out_of_service: bool = False,
    ) -> list[Object]:
        """Add a BI object to the emulator."""
        object_instance = object_type(
            instance=instance,
            name=name,
            description=description,
            presentValue=BinaryPV(initial_value),
        )
        object_instance.add_objects_to_application(self.device)
        if out_of_service:
            for _object in object_instance.objects.values():
                _object.outOfService = Boolean(out_of_service)
        self.objects_values[instance] = BinaryPV(initial_value)
        _objects = list(object_instance.objects.values())
        ObjectFactory.clear_objects()
        return _objects

    def run(self) -> None:
        """Run the loop of the BACnet emulator thread."""
        _LOGGER.debug("BACnet emulator thread started")
        while not self.stopped:
            for (
                object_type,
                object_id,
            ), _object in self.device.this_application.objectIdentifier.items():
                if (
                    object_type == "binaryOutput"
                    and (new_value := BinaryPV(_object.presentValue))
                    != self.objects_values[object_id]
                ):
                    if _object.outOfService == Boolean(True):
                        _LOGGER.debug(
                            "Object %s value updated to %s, but it is out of service",
                            object_id,
                            new_value,
                        )
                        _object.presentValue = self.objects_values[object_id]
                        continue
                    _LOGGER.debug("Object %s value updated to %s", object_id, new_value)
                    self.value_updated_cb(object_id, new_value)
                    self.objects_values[object_id] = new_value
            sleep(1)
