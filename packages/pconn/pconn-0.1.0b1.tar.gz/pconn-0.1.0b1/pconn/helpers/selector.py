"""Helpers for plugin entry flow."""

from collections.abc import Callable, Mapping, Sequence
from enum import StrEnum
from typing import Any, Generic, Literal, Required, TypedDict, TypeVar, cast
from uuid import UUID

import voluptuous as vol
import voluptuous_serialize

_T = TypeVar("_T", bound=Mapping[str, Any])


class Selector(Generic[_T]):
    """Base class for selectors."""

    CONFIG_SCHEMA: Callable
    config: _T
    selector_type: str

    def __init__(self, config: Mapping[str, Any] | None = None) -> None:
        """Instantiate a selector."""
        # Selectors can be empty
        if config is None:
            config = {}

        self.config = self.CONFIG_SCHEMA(config)

    def serialize(self) -> dict[str, dict[str, _T]]:
        """Serialize Selector for voluptuous_serialize."""
        return {"selector": {self.selector_type: self.config}}


class BooleanSelectorConfig(TypedDict):
    """Class to represent a boolean selector config."""


class BooleanSelector(Selector[BooleanSelectorConfig]):
    """Selector of a boolean value."""

    selector_type = "boolean"

    CONFIG_SCHEMA = vol.Schema({})

    def __init__(self, config: BooleanSelectorConfig | None = None) -> None:
        """Instantiate a selector."""
        super().__init__(config)

    def __call__(self, data: Any) -> bool:
        """Validate the passed selection."""
        value: bool = vol.Coerce(bool)(data)
        return value


class NumberSelectorConfig(TypedDict, total=False):
    """Class to represent a number selector config."""

    min: float
    max: float
    step: float | Literal["any"]
    unit_of_measurement: str


class NumberSelector(Selector[NumberSelectorConfig]):
    """Selector of a numeric value."""

    selector_type = "number"

    CONFIG_SCHEMA = vol.All(
        vol.Schema(
            {
                vol.Optional("min"): vol.Coerce(float),
                vol.Optional("max"): vol.Coerce(float),
                # Controls slider steps, and up/down keyboard binding for the box
                # user input is not rounded
                vol.Optional("step", default=1): vol.Any(
                    "any", vol.All(vol.Coerce(float), vol.Range(min=1e-3))
                ),
            }
        ),
    )

    def __init__(self, config: NumberSelectorConfig | None = None) -> None:
        """Instantiate a selector."""
        super().__init__(config)

    def __call__(self, data: Any) -> float:
        """Validate the passed selection."""
        value: float = vol.Coerce(float)(data)

        if "min" in self.config and value < self.config["min"]:
            raise vol.Invalid(f"Value {value} is too small")

        if "max" in self.config and value > self.config["max"]:
            raise vol.Invalid(f"Value {value} is too large")

        return value


select_option = vol.All(
    dict,
    vol.Schema(
        {
            vol.Required("value"): str,
            vol.Required("label"): str,
        }
    ),
)


class SelectOptionDict(TypedDict):
    """Class to represent a select option dict."""

    value: str
    label: str


class SelectSelectorMode(StrEnum):
    """Possible modes for a number selector."""

    LIST = "list"
    DROPDOWN = "dropdown"


class SelectSelectorConfig(TypedDict, total=False):
    """Class to represent a select selector config."""

    options: Required[Sequence[SelectOptionDict] | Sequence[str]]
    multiple: bool
    custom_value: bool
    mode: SelectSelectorMode
    translation_key: str
    sort: bool


class SelectSelector(Selector[SelectSelectorConfig]):
    """Selector for an single-choice input select."""

    selector_type = "select"

    CONFIG_SCHEMA = vol.Schema(
        {
            vol.Required("options"): vol.All(vol.Any([str], [select_option])),
            vol.Optional("multiple", default=False): bool,
            vol.Optional("custom_value", default=False): bool,
            vol.Optional("mode"): vol.All(
                vol.Coerce(SelectSelectorMode), lambda val: val.value
            ),
            vol.Optional("sort", default=False): bool,
        }
    )

    def __init__(self, config: SelectSelectorConfig | None = None) -> None:
        """Instantiate a selector."""
        super().__init__(config)

    def __call__(self, data: Any) -> Any:
        """Validate the passed selection."""
        options: Sequence[str] = []
        if config_options := self.config["options"]:
            if isinstance(config_options[0], str):
                options = cast(Sequence[str], config_options)
            else:
                options = [
                    option["value"]
                    for option in cast(Sequence[SelectOptionDict], config_options)
                ]

        parent_schema = vol.In(options)
        if self.config["custom_value"]:
            parent_schema = vol.Any(parent_schema, str)

        if not self.config["multiple"]:
            return parent_schema(vol.Schema(str)(data))
        if not isinstance(data, list):
            raise vol.Invalid("Value should be a list")
        return [parent_schema(vol.Schema(str)(val)) for val in data]


class TextSelectorType(StrEnum):
    """Enum for text selector types."""

    COLOR = "color"
    DATE = "date"
    DATETIME_LOCAL = "datetime-local"
    EMAIL = "email"
    MONTH = "month"
    NUMBER = "number"
    PASSWORD = "password"
    SEARCH = "search"
    TEL = "tel"
    TEXT = "text"
    TIME = "time"
    URL = "url"
    WEEK = "week"


class TextSelectorConfig(TypedDict, total=False):
    """Class to represent a text selector config."""

    multiline: bool
    prefix: str
    suffix: str
    type: TextSelectorType
    autocomplete: str
    multiple: bool


class TextSelector(Selector[TextSelectorConfig]):
    """Selector for a multi-line text string."""

    selector_type = "text"

    CONFIG_SCHEMA = vol.Schema(
        {
            vol.Optional("multiline", default=False): bool,
            vol.Optional("prefix"): str,
            vol.Optional("suffix"): str,
            # The "type" controls the input field in the browser, the resulting
            # data can be any string so we don't validate it.
            vol.Optional("type"): vol.All(
                vol.Coerce(TextSelectorType), lambda val: val.value
            ),
            vol.Optional("autocomplete"): str,
            vol.Optional("multiple", default=False): bool,
        }
    )

    def __init__(self, config: TextSelectorConfig | None = None) -> None:
        """Instantiate a selector."""
        super().__init__(config)

    def __call__(self, data: Any) -> str | list[str]:
        """Validate the passed selection."""
        if not self.config["multiple"]:
            text: str = vol.Schema(str)(data)
            return text
        if not isinstance(data, list):
            raise vol.Invalid("Value should be a list")
        return [vol.Schema(str)(val) for val in data]


class FileSelectorConfig(TypedDict):
    """Class to represent a file selector config."""

    accept: str  # required


class FileSelector(Selector[FileSelectorConfig]):
    """Selector of a file."""

    selector_type = "file"

    CONFIG_SCHEMA = vol.Schema(
        {
            # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#accept
            vol.Required("accept"): str,
        }
    )

    def __init__(self, config: FileSelectorConfig) -> None:
        """Instantiate a selector."""
        super().__init__(config)

    def __call__(self, data: Any) -> str:
        """Validate the passed selection."""
        if not isinstance(data, str):
            raise vol.Invalid("Value should be a string")

        UUID(data)

        return data


def custom_serializer(schema: Any) -> Any:
    """Serialize additional types for voluptuous_serialize."""

    if isinstance(schema, Selector):
        return schema.serialize()

    return voluptuous_serialize.UNSUPPORTED
