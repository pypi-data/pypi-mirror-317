"""Demo plugin flow handler."""

from __future__ import annotations

from typing import Any

from BAC0.core.io.IOExceptions import InitializationError
import voluptuous as vol

from pconn.const import CONF_HOST, CONF_ID, CONF_PORT
from pconn.helpers import selector
from pconn.plugin_entries import PluginEntryFlow
from pconn.plugin_entry_flow import FlowResult

from . import DOMAIN
from .bacnet_device import create_device
from .const import CONF_BBMD_ADDRESS, DEFAULT_DEVICE_ID, DEFAULT_PORT


class BACnetEmulatorFlowHandler(PluginEntryFlow, domain=DOMAIN):
    """BACnet emulator Plugin flow handler."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle plugin setup."""

        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                device = create_device(
                    ip=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                    deviceId=user_input[CONF_ID],
                    bbmdAddress=user_input.get(CONF_BBMD_ADDRESS),
                )
                device.disconnect()
            except InitializationError:
                errors["base"] = "cannot_connect"

            else:
                return self.async_create_entry(title="BACnet Emulator", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): selector.TextSelector(
                        selector.TextSelectorConfig()
                    ),
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(
                        selector.NumberSelector(), vol.Coerce(int)
                    ),
                    vol.Required(CONF_ID, default=DEFAULT_DEVICE_ID): vol.All(
                        selector.NumberSelector(), vol.Coerce(int)
                    ),
                    vol.Optional(CONF_BBMD_ADDRESS): selector.TextSelector(
                        selector.TextSelectorConfig()
                    ),
                }
            ),
            errors=errors,
        )
