"""Constants for Gallagher plugins."""

from typing import Final

VERSION = "0.1.0b1"
CONFIG_DIR = "config"
CORE_CONFIG = "core.config"
PLUGINS_ENTRIES = "plugins.entries"

# Date/Time formats
FORMAT_DATE = "%Y-%m-%d"
FORMAT_TIME = "%H:%M:%S"
FORMAT_DATETIME = f"{FORMAT_DATE} {FORMAT_TIME}"

PLUGIN_FLOWS = "plugin_flows"
PLUGIN_MODULES = "plugin_modules"
GLL_CLIENTS = "gll_clients"
CORE = "core"

DATA_LOGGING = "logging"
# Version
MAJOR_VERSION: Final = 2025
MINOR_VERSION: Final = 1
PATCH_VERSION: Final = 0
__short_version__: Final = f"{MAJOR_VERSION}.{MINOR_VERSION}"
__version__: Final = f"{__short_version__}.{PATCH_VERSION}"


# CONFIG
CONF_API_KEY: Final = "api_key"
CONF_API_TOKEN: Final = "api_token"
CONF_EMAIL: Final = "email"
CONF_FILE_PATH: Final = "file_path"
CONF_HOST: Final = "host"
CONF_ID: Final = "id"
CONF_IP_ADDRESS: Final = "ip_address"
CONF_NAME: Final = "name"
CONF_PASSWORD: Final = "password"
CONF_PATH: Final = "path"
CONF_PORT: Final = "port"
CONF_PROTOCOL: Final = "protocol"
CONF_SCAN_INTERVAL: Final = "scan_interval"
CONF_SELECTOR: Final = "selector"
CONF_USERNAME: Final = "username"
CONF_UPDATE_INTERVAL: Final = "update_interval"
CONF_USE_SSL: Final = "use_ssl"

SIGNAL_DATA_UPDATED: Final = "data-updated"
SIGNAL_STATUS_UPDATED: Final = "status-updated"
