"""Demo plugin to show functionalities."""

import BAC0
from gallagher_restapi import Client

from pconn.core import PConn
from pconn.exceptions import PluginEntryError
from pconn.plugin_entries import PluginEntry
from pconn.plugins.bacnet_emulator import DOMAIN as BACNET_EMULATOR
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST

from .plugin import BACnetEmulator, GallagherBACnetEmulator


async def async_setup_entry(
    pconn: PConn, entry: PluginEntry[GallagherBACnetEmulator]
) -> bool:
    """Setup demo plugin from config."""
    if not (
        gll_rest_entry := await pconn.plugin_entries.async_get_platform_entry(
            entry, GALLAGHER_REST
        )
    ):
        raise PluginEntryError("Gallagher REST entry is not available.")
    gll_client: Client = gll_rest_entry.plugin_data

    if not (
        bacnet_emulator := await pconn.plugin_entries.async_get_platform_entry(
            entry, BACNET_EMULATOR
        )
    ):
        raise PluginEntryError("BACnet Emulator entry is not available.")
    bacnet_device: BAC0.lite = bacnet_emulator.plugin_data

    plugin = GallagherBACnetEmulator(pconn, entry, gll_client, bacnet_device)
    await plugin.initialize_items()
    entry.plugin_data = plugin

    entry.async_on_unload(entry.add_update_listener(async_options_updated))

    return True


async def async_unload_entry(
    pconn: PConn, entry: PluginEntry[GallagherBACnetEmulator]
) -> bool:
    """Unload plugin from plugin entry."""
    plugin: BACnetEmulator = entry.plugin_data
    plugin.device.device.disconnect()
    plugin.device.stopped = True
    return True


async def async_options_updated(
    pconn: PConn, entry: PluginEntry[GallagherBACnetEmulator]
) -> None:
    """Plugin entry options updated."""
    await pconn.plugin_entries.async_reload(entry.entry_id)
