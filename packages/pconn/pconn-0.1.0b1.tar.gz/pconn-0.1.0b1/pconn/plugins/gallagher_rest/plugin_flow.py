"""Demo plugin flow handler."""

from __future__ import annotations

from typing import Any

from gallagher_restapi import GllApiError
from gallagher_restapi.exceptions import UnauthorizedError
import voluptuous as vol

from pconn.const import CONF_API_KEY, CONF_API_TOKEN, CONF_HOST, CONF_PORT, CONF_USE_SSL
from pconn.helpers import httpx_client, selector
from pconn.plugin_entries import PluginEntryFlow
from pconn.plugin_entry_flow import FlowResult
from pconn.plugins.gallagher_rest import get_gll_client

from . import DOMAIN
from .const import (
    CLOUD_GATEWAYS,
    CONF_CLOUD_GATEWAY,
    DEFAULT_CLOUD_GATEWAY,
    DEFAULT_PORT,
    PLACEHOLDER_CERT_THUMBPRINT,
)

BASE_CONFIG_FIELDS = {
    vol.Required(CONF_API_KEY): selector.TextSelector(
        selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
    ),
    vol.Optional(CONF_API_TOKEN): selector.TextSelector(
        selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
    ),
    vol.Optional(CONF_USE_SSL, default=False): selector.BooleanSelector(),
}

CLOUD_CONFIG_FIELDS = {
    vol.Required(
        CONF_CLOUD_GATEWAY, default=DEFAULT_CLOUD_GATEWAY
    ): selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[
                selector.SelectOptionDict(label=key, value=value)
                for key, value in CLOUD_GATEWAYS.items()
            ]
        )
    )
}

LOCAL_CONFIG_FIELDS = {
    vol.Optional(CONF_HOST, default="localhost"): selector.TextSelector(
        selector.TextSelectorConfig(autocomplete="host")
    ),
    vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(
        selector.NumberSelector(), vol.Coerce(int)
    ),
}


class GallagherRESTFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """Demo Plugin flow handler."""

    def __init__(self) -> None:
        """Initialize flow handler."""
        self.data: dict[str, Any] = {}

    async def validate_input(self, user_input: dict[str, Any]) -> dict[str, Any]:
        """Validate connection to Gallagher server."""
        errors = {}
        gll_client = get_gll_client(self.pconn, **user_input)
        try:
            await gll_client.initialize()
        except UnauthorizedError:
            errors["base"] = "unauthorized_error"
        except GllApiError:
            errors["base"] = "connection_error"
        return errors

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle init step."""
        return self.async_show_menu(step_id="init", menu_options=["local", "cloud"])

    async def async_step_local(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle local step."""
        errors = {}
        if user_input is not None:
            if user_input[CONF_USE_SSL]:
                self.data = user_input
                return await self.async_step_ssl()
            if not (errors := await self.validate_input(user_input)):
                return self.async_create_entry(
                    title=f"Gallagher ({user_input[CONF_HOST]})", data=user_input
                )

        return self.async_show_form(
            step_id="local",
            data_schema=vol.Schema({**LOCAL_CONFIG_FIELDS, **BASE_CONFIG_FIELDS}),
            errors=errors,
        )

    async def async_step_cloud(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle cloud step."""
        errors = {}
        if user_input is not None:
            if user_input[CONF_USE_SSL]:
                self.data = user_input
                return await self.async_step_ssl()
            if not (errors := await self.validate_input(user_input)):
                return self.async_create_entry(
                    title=f"Gallagher ({user_input.get(CONF_HOST)})", data=user_input
                )

        return self.async_show_form(
            step_id="cloud",
            data_schema=vol.Schema({**CLOUD_CONFIG_FIELDS, **BASE_CONFIG_FIELDS}),
            errors=errors,
        )

    async def async_step_ssl(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle ssl step."""
        errors = {}
        if user_input is not None:
            if not (errors := await self.validate_input(self.data)):
                return self.async_create_entry(
                    title=f"Gallagher ({self.data.get(CONF_HOST)})", data=self.data
                )

        thumbprint = await self.pconn.async_add_executor_job(
            httpx_client.create_self_signed_cert, self.pconn
        )
        return self.async_show_form(
            step_id="ssl",
            description_placeholders={PLACEHOLDER_CERT_THUMBPRINT: thumbprint},
            errors=errors,
        )
