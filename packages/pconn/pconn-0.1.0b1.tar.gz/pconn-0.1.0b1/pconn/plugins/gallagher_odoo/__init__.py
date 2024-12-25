"""Plugin for interfacing with Odoo system."""

from gallagher_restapi import Client

from pconn.core import PConn
from pconn.exceptions import PluginEntryError
from pconn.plugin_entries import PluginEntry
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST
from pconn.plugins.odoo import DOMAIN as ODOO

from .client import OdooClient
from .errors import ConfigError
from .plugin import Odoo


async def async_setup_entry(pconn: PConn, entry: PluginEntry[Odoo]) -> bool:
    """Setup plugin from plugin entry."""
    if not (
        gll_rest_entry := await pconn.plugin_entries.async_get_platform_entry(
            entry, GALLAGHER_REST
        )
    ):
        raise PluginEntryError("Gallagher REST entry is not available.")
    gll_client: Client = gll_rest_entry.plugin_data

    if not (
        odoo_entry := await pconn.plugin_entries.async_get_platform_entry(entry, ODOO)
    ):
        raise PluginEntryError("Odoo entry is not available.")
    odoo_client: OdooClient = odoo_entry.plugin_data

    plugin = Odoo(pconn, entry, gll_client, odoo_client)
    try:
        await plugin.async_initialize()
    except ConfigError as err:
        raise PluginEntryError(str(err)) from err
    entry.plugin_data = plugin

    entry.async_on_unload(entry.add_update_listener(async_options_updated))

    return True


async def async_options_updated(pconn: PConn, entry: PluginEntry[Odoo]) -> None:
    """Plugin entry options updated."""
    await pconn.plugin_entries.async_reload(entry.entry_id)
