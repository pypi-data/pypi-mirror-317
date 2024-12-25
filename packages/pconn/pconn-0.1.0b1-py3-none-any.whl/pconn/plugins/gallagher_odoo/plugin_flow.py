"""Demo plugin flow handler."""

from __future__ import annotations

from typing import Any

from gallagher_restapi import GllApiError
import voluptuous as vol

from pconn import plugin_entry_flow
from pconn.helpers import selector
from pconn.plugin_entries import PluginEntry, PluginEntryFlow, PluginOptionsFlow
from pconn.plugins.gallagher_rest import DOMAIN as GALLAGHER_REST
from pconn.plugins.odoo import DOMAIN as ODOO, OdooError

from .const import (
    CONF_GLL_UNIQUE_PDF,
    CONF_ODOO_UNIQUE_FIELD,
    CONF_ONE_READER_DOORS,
    CONF_TWO_READER_DOORS,
)
from .plugin import DOMAIN, Odoo

DEFAULT_PROTOCOL = "http"
PROTOCOL_CHOICES = ["https", "http"]


class OdooFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """Odoo Plugin flow handler."""

    PLATFORMS = [GALLAGHER_REST, ODOO]

    @staticmethod
    def async_get_options_flow(
        plugin_entry: PluginEntry,
    ) -> OdooOptionsFlowHandler:
        """Get the options flow for this handler."""
        return OdooOptionsFlowHandler(plugin_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> plugin_entry_flow.FlowResult:
        """Handle plugin onboarding."""
        return self.async_create_entry(title="Gallagher Odoo", data={})


class OdooOptionsFlowHandler(PluginOptionsFlow):
    """Handle Odoo plugin options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> plugin_entry_flow.FlowResult:
        """Manage options."""
        errors = {}
        if user_input is not None:
            if not (
                user_input.get(CONF_ONE_READER_DOORS)
                or user_input.get(CONF_TWO_READER_DOORS)
            ):
                errors["base"] = "Must select at least one door"
            elif user_input.get(CONF_ONE_READER_DOORS) == user_input.get(
                CONF_TWO_READER_DOORS
            ):
                errors[CONF_ONE_READER_DOORS] = errors[CONF_TWO_READER_DOORS] = (
                    "Found same door in both lists"
                )
            if not errors:
                return self.async_create_entry(title="", data=user_input)

        odoo_plugin: Odoo = self.plugin_entry.plugin_data
        try:
            odoo_unique_pdfs = await odoo_plugin.async_get_odoo_unique_fields()
            gll_unique_pdfs = await odoo_plugin.async_get_gll_unique_fields()
            doors = await odoo_plugin.async_get_doors()
        except GllApiError:
            return self.async_abort(reason="gallagher_connection_error")
        except OdooError:
            return self.async_abort(reason="odoo_connection_error")
        options = {
            vol.Required(
                CONF_GLL_UNIQUE_PDF,
                default=self.plugin_entry.options.get(CONF_GLL_UNIQUE_PDF),
            ): (
                selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=pdf.id, label=pdf.name)
                            for pdf in gll_unique_pdfs
                        ],
                    )
                )
            ),
            vol.Required(
                CONF_ODOO_UNIQUE_FIELD,
                default=self.plugin_entry.options.get(CONF_ODOO_UNIQUE_FIELD),
            ): (
                selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(label=label, value=field)
                            for field, label in odoo_unique_pdfs.items()
                        ],
                    )
                )
            ),
            vol.Optional(
                CONF_ONE_READER_DOORS,
                default=self.plugin_entry.options.get(CONF_ONE_READER_DOORS, []),
            ): (
                selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=id, label=name)
                            for id, name in doors.items()
                        ],
                        multiple=True,
                    )
                )
            ),
            vol.Optional(
                CONF_TWO_READER_DOORS,
                default=self.plugin_entry.options.get(CONF_TWO_READER_DOORS, []),
            ): (
                selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=id, label=name)
                            for id, name in doors.items()
                        ],
                        multiple=True,
                    )
                )
            ),
        }
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(options),
            errors=errors,
        )
