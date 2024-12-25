"""Demo plugin flow handler."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from pconn.helpers import selector
from pconn.plugin_entries import PluginEntry, PluginEntryFlow, PluginOptionsFlow
from pconn.plugin_entry_flow import FlowResult
from pconn.plugins.bacnet_emulator import DOMAIN as BACNET_EMULATOR
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST

from .const import CONF_MONITORED_ITEM_TYPES, DOMAIN


class BACnetEmulatorFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """BACnet emulator Plugin flow handler."""

    PLATFORMS = [GALLAGHER_REST, BACNET_EMULATOR]

    @staticmethod
    def async_get_options_flow(
        plugin_entry: PluginEntry,
    ) -> BACnetEmulatorOptionsFlowHandler:
        """Get the options flow for this handler."""
        return BACnetEmulatorOptionsFlowHandler(plugin_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle plugin setup."""
        return self.async_create_entry(title="Gallagher BACnet Emulator", data={})


class BACnetEmulatorOptionsFlowHandler(PluginOptionsFlow):
    """Handle plugin options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Optional(
                item_type,
                default=self.plugin_entry.options.get(item_type, False),
            ): selector.BooleanSelector()
            for item_type in CONF_MONITORED_ITEM_TYPES
        }
        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
