"""Demo plugin flow handler."""

from __future__ import annotations

from typing import Any

from google.api_core.exceptions import InvalidArgument
import google.generativeai as genai
import voluptuous as vol

from pconn.const import CONF_API_KEY
from pconn.helpers import selector
from pconn.plugin_entries import PluginEntryFlow
from pconn.plugin_entry_flow import FlowResult

from . import DOMAIN


class AIAnalyzerFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """AI Analyzer platform flow handler."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle plugin onboarding."""
        errors = {}
        if user_input is not None:
            genai.configure(api_key=user_input[CONF_API_KEY])
            model = genai.GenerativeModel()
            try:
                response = model.generate_content("Say yes if you are working.")
            except InvalidArgument:
                errors["base"] = "invalid_api_key"
            if "yes" not in response.text.lower():
                errors["base"] = "unauthorized_error"
            else:
                return self.async_create_entry(title="Gallagher", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        )
                    )
                }
            ),
            errors=errors,
        )
