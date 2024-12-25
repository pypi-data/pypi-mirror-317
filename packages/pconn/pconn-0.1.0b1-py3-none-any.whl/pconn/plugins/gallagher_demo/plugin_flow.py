"""Demo plugin flow handler."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from pconn.core import TYPE_CHECKING
from pconn.helpers import selector
from pconn.plugin_entries import PluginEntry, PluginEntryFlow, PluginOptionsFlow
from pconn.plugin_entry_flow import FlowResult
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST

if TYPE_CHECKING:
    from . import Demo
from .const import DOMAIN, PHOTO_PDF, TITLE


class DemoFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """Demo Plugin flow handler."""

    PLATFORMS = [GALLAGHER_REST]

    @staticmethod
    def async_get_options_flow(
        plugin_entry: PluginEntry,
    ) -> DemoOptionsFlowHandler:
        """Get the options flow for this handler."""
        return DemoOptionsFlowHandler(plugin_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle plugin onboarding."""
        return self.async_create_entry(title=TITLE, data={})


class DemoOptionsFlowHandler(PluginOptionsFlow):
    """Handle Demo plugin options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        demo_plugin: Demo = self.plugin_entry.plugin_data
        photo_pdfs = demo_plugin.get_photo_pdfs()
        options = {
            vol.Required(
                PHOTO_PDF, default=self.plugin_entry.options.get(PHOTO_PDF, None)
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        selector.SelectOptionDict(label=pdf.name, value=pdf.id)
                        for pdf in photo_pdfs
                    ],
                )
            )
        }
        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
