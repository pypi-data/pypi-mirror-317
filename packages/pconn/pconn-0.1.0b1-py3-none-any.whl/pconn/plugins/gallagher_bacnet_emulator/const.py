"""Constants for the BACnet Emulator plugin."""

from typing import Final

DOMAIN: Final = "gallagher_bacnet_emulator"
CONTROLLERS: Final = "controllers"
INPUTS: Final = "inputs"
OUTPUTS: Final = "outputs"
CONF_MONITORED_ITEM_TYPES: Final = [CONTROLLERS, INPUTS, OUTPUTS]
