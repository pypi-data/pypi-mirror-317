"""Demo plugin to show functionalities."""

from gallagher_restapi import Client
import google.generativeai as genai

from pconn.core import PConn
from pconn.exceptions import PluginEntryError
from pconn.plugin_entries import PluginEntry
from pconn.plugins.ai_analyzer import DOMAIN as AI_ANALYZER
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST

from .plugin import GallagherAIAnalyzer


async def async_setup_entry(
    pconn: PConn, entry: PluginEntry[GallagherAIAnalyzer]
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
        ai_analyzer_entry := await pconn.plugin_entries.async_get_platform_entry(
            entry, AI_ANALYZER
        )
    ):
        raise PluginEntryError("AI Analyzer platform entry is not loaded")

    ai_model: genai.GenerativeModel = ai_analyzer_entry.plugin_data

    plugin = GallagherAIAnalyzer(pconn, entry, gll_client, ai_model)
    entry.plugin_data = plugin

    entry.async_on_unload(entry.add_update_listener(async_options_updated))

    return True


async def async_options_updated(
    pconn: PConn, entry: PluginEntry[GallagherAIAnalyzer]
) -> None:
    """Plugin entry options updated."""
    await pconn.plugin_entries.async_reload(entry.entry_id)
