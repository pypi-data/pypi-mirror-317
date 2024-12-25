"""Constants for the BACnet Emulator plugin."""

from typing import Final

CONF_BBMD_ADDRESS: Final = "bbmd_address"
CONTROLLERS: Final = "controllers"
INPUTS: Final = "inputs"
OUTPUTS: Final = "outputs"
CONF_MONITORED_ITEM_TYPES: Final = [CONTROLLERS, INPUTS, OUTPUTS]

CONF_REGISTERED_ITEMS: Final = "registered_items"
CONF_DISABLED_ITEMS: Final = "disabled_items"
CONF_NEW_ID: Final = "last_id"


DEFAULT_PORT: Final = 47808
DEFAULT_DEVICE_ID: Final = 89089
