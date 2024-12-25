"""Demo plugin to show functionalities."""

import BAC0
from BAC0.core.io.IOExceptions import InitializationError

from pconn.const import CONF_HOST, CONF_ID, CONF_PORT
from pconn.core import PConn
from pconn.exceptions import PluginEntryError
from pconn.plugin_entries import PluginEntry

from .bacnet_device import create_device
from .const import CONF_BBMD_ADDRESS

DOMAIN = "bacnet_emulator"


async def async_setup_entry(pconn: PConn, entry: PluginEntry[BAC0.lite]) -> bool:
    """Setup bacnet emulator from config."""
    try:
        bacnet_device = create_device(
            ip=entry.data[CONF_HOST],
            port=entry.data[CONF_PORT],
            deviceId=entry.data[CONF_ID],
            bbmdAddress=entry.data.get(CONF_BBMD_ADDRESS),
        )
    except InitializationError as err:
        raise PluginEntryError(str(err)) from err

    entry.plugin_data = bacnet_device

    return True
