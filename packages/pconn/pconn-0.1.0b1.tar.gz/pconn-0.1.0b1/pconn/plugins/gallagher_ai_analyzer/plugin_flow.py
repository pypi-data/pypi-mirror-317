"""Demo plugin flow handler."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from pconn.helpers import selector
from pconn.plugin_entries import PluginEntry, PluginEntryFlow, PluginOptionsFlow
from pconn.plugin_entry_flow import FlowResult
from pconn.plugins.ai_analyzer import DOMAIN as AI_ANALYZER
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST

from .const import CONF_DATA_TYPES, DATA_TYPES, DOMAIN, TITLE


class GallagherAIAnalyzerFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """Gallagher AI Analyzer Plugin flow handler."""

    PLATFORMS = [GALLAGHER_REST, AI_ANALYZER]

    @staticmethod
    def async_get_options_flow(
        plugin_entry: PluginEntry,
    ) -> GallagherAIAnalyzerOptionsFlowHandler:
        """Get the options flow for this handler."""
        return GallagherAIAnalyzerOptionsFlowHandler(plugin_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle plugin onboarding."""
        return self.async_create_entry(title=TITLE, data={})


class GallagherAIAnalyzerOptionsFlowHandler(PluginOptionsFlow):
    """Handle Demo plugin options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Required(
                CONF_DATA_TYPES,
                default=self.plugin_entry.options.get(CONF_DATA_TYPES, None),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        selector.SelectOptionDict(value=value, label=label)
                        for value, label in DATA_TYPES.items()
                    ],
                    multiple=True,
                )
            )
        }
        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
