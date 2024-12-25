"""Constants for Gallagher REST platform."""

from typing import Final

CONF_CONNECTION: Final = "connection"

CONF_GLL_UNIQUE_PDF: Final = "gll_unique_pdf"
CONF_DIVISION: Final = "division"
CONF_CLOUD_GATEWAY: Final = "cloud_gateway"
DEFAULT_CLOUD_GATEWAY: Final = "AU_GATEWAY"

PLACEHOLDER_CERT_THUMBPRINT: Final = "thumbprint"

CLOUD_GATEWAYS: Final = {"AU Gateway": "AU_GATEWAY", "US Gateway": "US_GATEWAY"}
DEFAULT_CONNECTION: Final = "local"
DEFAULT_PORT: Final = 8904

CONTROLLER_TYPES: Final = [
    "Controller 6000",
    "Controller 7000",
    "Controller 7000 Single Door",
]

READER_TYPES: Final = ["HBUS Reader", "HBUS Terminal"]

DOOR_TYPES: Final = [
    "Door",
]

UNAVAILABLE_FLAGS: Final = [
    "controllerOffline",
    "controllerUnknown",
    "notPolled",
    "processOffline",
    "deviceNotResponding",
]
