"""Demo plugin to show functionalities."""

from gallagher_restapi import Client

from pconn.core import PConn
from pconn.exceptions import PluginEntryError
from pconn.plugin_entries import PluginEntry
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST

from .plugin import Demo


async def async_setup_entry(pconn: PConn, entry: PluginEntry[Demo]) -> bool:
    """Setup demo plugin from config."""
    if not (
        gll_rest_entry := await pconn.plugin_entries.async_get_platform_entry(
            entry, GALLAGHER_REST
        )
    ):
        raise PluginEntryError("Gallagher REST entry is not available.")
    gll_client: Client = gll_rest_entry.plugin_data

    plugin = Demo(pconn, entry, gll_client)
    await plugin.async_initialize()
    entry.plugin_data = plugin

    return True
