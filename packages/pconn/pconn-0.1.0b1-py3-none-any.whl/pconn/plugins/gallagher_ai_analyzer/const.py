"""Constants for Demo plugin."""

from enum import StrEnum
from typing import Final

from pconn.plugins.gallagher_rest.const import CONTROLLER_TYPES, READER_TYPES

DOMAIN: Final = "gallagher_ai_analyzer"
TITLE: Final = "Gallagher AI Analyzer"

CONF_DATA_TYPES: Final = "data_types"


class DataType(StrEnum):
    """Data types enum."""

    ALARMS = "alarms"
    CARDHOLDERS = "cardholders"
    CARDHOLDER_EVENTS = "cardholder events"
    CONTROLLERS = "controllers"
    DOORS = "doors"
    READERS = "readers"
    NONE = "none"


DATA_TYPES: Final = {
    DataType.ALARMS: "Alarms",
    DataType.CARDHOLDERS: "Cardholders",
    DataType.CARDHOLDER_EVENTS: "Cardholder Events",
    DataType.CONTROLLERS: "Controllers",
    DataType.DOORS: "Doors",
    DataType.READERS: "Readers",
}

ITEM_TYPES = {
    DataType.CONTROLLERS: CONTROLLER_TYPES,
    DataType.READERS: READER_TYPES,
    DataType.DOORS: ["Door"],
}
