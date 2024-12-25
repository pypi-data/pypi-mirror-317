"""Demo plugin flow handler."""

from typing import Any

import voluptuous as vol

from pconn import plugin_entry_flow
from pconn.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_USERNAME,
)
from pconn.core import PConn
from pconn.helpers import selector
from pconn.plugin_entries import PluginEntryFlow

from . import DOMAIN, OdooClient
from .errors import ConfigError, ConnectError, InvalidAuth

DEFAULT_PROTOCOL = "http"
PROTOCOL_CHOICES = ["https", "http"]
CONF_DB_NAME = "db_name"
DEFAULT_PORT = "8069"


async def async_validate(pconn: PConn, user_input: dict[str, Any]) -> dict[str, Any]:
    """Validate user input and return errors if any."""
    errors: dict[str, Any] = {}
    client = OdooClient(**user_input)
    try:
        await pconn.async_add_executor_job(client.connect)
    except InvalidAuth:
        errors["base"] = "auth_error"
    except ConfigError:
        errors["base"] = "db_error"
    except ConnectError:
        errors["base"] = "cannot_connect"
    return errors


class OdooFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """Odoo platform flow handler."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> plugin_entry_flow.FlowResult:
        """Handle plugin onboarding."""
        errors = {}
        if user_input is not None:
            errors = await async_validate(self.pconn, user_input)
            if not errors:
                return self.async_create_entry(
                    title=f"Odoo ({user_input[CONF_HOST]})", data=user_input
                )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PROTOCOL, default=DEFAULT_PROTOCOL
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(options=PROTOCOL_CHOICES)
                    ),
                    vol.Required(CONF_HOST): selector.TextSelector(
                        selector.TextSelectorConfig(autocomplete="host")
                    ),
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(
                        selector.NumberSelector(), vol.Coerce(int)
                    ),
                    vol.Required(CONF_DB_NAME): selector.TextSelector(),
                    vol.Required(CONF_USERNAME): selector.TextSelector(
                        selector.TextSelectorConfig(autocomplete="username")
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        )
                    ),
                }
            ),
            errors=errors,
        )
