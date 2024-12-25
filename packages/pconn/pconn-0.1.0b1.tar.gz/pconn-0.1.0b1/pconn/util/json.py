"""JSON utility functions."""

from __future__ import annotations

from collections.abc import Callable
import datetime
import logging
import os
from os import PathLike
from pathlib import Path
import tempfile
from typing import Any

import orjson

from pconn.exceptions import PConnError

_SENTINEL = object()
_LOGGER = logging.getLogger(__name__)

JsonValueType = (
    dict[str, "JsonValueType"] | list["JsonValueType"] | str | int | float | bool | None
)
"""Any data that can be returned by the standard JSON deserializing process."""
JsonArrayType = list[JsonValueType]
"""List that can be returned by the standard JSON deserializing process."""
JsonObjectType = dict[str, JsonValueType]
"""Dictionary that can be returned by the standard JSON deserializing process."""

JSON_ENCODE_EXCEPTIONS = (TypeError, ValueError)
JSON_DECODE_EXCEPTIONS = (orjson.JSONDecodeError,)


class SerializationError(PConnError):
    """Error serializing the data to JSON."""


json_loads: Callable[[bytes | bytearray | memoryview | str], JsonValueType]
json_loads = orjson.loads
"""Parse JSON data."""


def json_loads_array(__obj: bytes | bytearray | memoryview | str) -> JsonArrayType:
    """Parse JSON data and ensure result is a list."""
    value: JsonValueType = json_loads(__obj)
    # Avoid isinstance overhead as we are not interested in list subclasses
    if type(value) is list:  # noqa: E721
        return value
    raise ValueError(f"Expected JSON to be parsed as a list got {type(value)}")


def json_loads_object(__obj: bytes | bytearray | memoryview | str) -> JsonObjectType:
    """Parse JSON data and ensure result is a dictionary."""
    value: JsonValueType = json_loads(__obj)
    # Avoid isinstance overhead as we are not interested in dict subclasses
    if type(value) is dict:  # noqa: E721
        return value
    raise ValueError(f"Expected JSON to be parsed as a dict got {type(value)}")


def load_json(
    filename: str | PathLike,
    default: JsonValueType = _SENTINEL,  # type: ignore[assignment]
) -> JsonValueType:
    """Load JSON data from a file.

    Defaults to returning empty dict if file is not found.
    """
    try:
        with open(filename, encoding="utf-8") as fdesc:
            return orjson.loads(fdesc.read())  # type: ignore[no-any-return]
    except FileNotFoundError:
        # This is not a fatal error
        _LOGGER.debug("JSON file not found: %s", filename)
    except ValueError as error:
        _LOGGER.exception("Could not parse JSON content: %s", filename)
        raise PConnError(error) from error
    except OSError as error:
        _LOGGER.exception("JSON file reading failed: %s", filename)
        raise PConnError(error) from error
    return {} if default is _SENTINEL else default


def load_json_array(
    filename: str | PathLike,
    default: JsonArrayType = _SENTINEL,  # type: ignore[assignment]
) -> JsonArrayType:
    """Load JSON data from a file and return as list.

    Defaults to returning empty list if file is not found.
    """
    if default is _SENTINEL:
        default = []
    value: JsonValueType = load_json(filename, default=default)
    # Avoid isinstance overhead as we are not interested in list subclasses
    if type(value) is list:  # noqa: E721
        return value
    _LOGGER.exception(
        "Expected JSON to be parsed as a list got %s in: %s", {type(value)}, filename
    )
    raise PConnError(
        f"Expected JSON to be parsed as a list got {type(value)}"
    )


def load_json_object(
    filename: str | PathLike,
    default: JsonObjectType = _SENTINEL,  # type: ignore[assignment]
) -> JsonObjectType:
    """Load JSON data from a file and return as dict.

    Defaults to returning empty dict if file is not found.
    """
    if default is _SENTINEL:
        default = {}
    value: JsonValueType = load_json(filename, default=default)
    # Avoid isinstance overhead as we are not interested in dict subclasses
    if type(value) is dict:  # noqa: E721
        return value
    _LOGGER.exception(
        "Expected JSON to be parsed as a dict got %s in: %s", {type(value)}, filename
    )
    raise PConnError(
        f"Expected JSON to be parsed as a dict got {type(value)}"
    )


def json_encoder_default(obj: Any) -> Any:
    """Convert Home Assistant objects.

    Hand other objects to the original method.
    """
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, float):
        return float(obj)
    if hasattr(obj, "as_dict"):
        return obj.as_dict()
    if isinstance(obj, Path):
        return obj.as_posix()
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError


def _orjson_default_encoder(data: Any) -> str:
    """JSON encoder that uses orjson with hass defaults."""
    return orjson.dumps(
        data,
        option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS,
        default=json_encoder_default,
    ).decode("utf-8")


def write_utf8_file(
    filename: str,
    utf8_data: str,
    private: bool = False,
) -> None:
    """Write a file and rename it into place.

    Writes all or nothing.
    """

    tmp_filename = ""
    try:
        # Modern versions of Python tempfile create this file with mode 0o600
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=os.path.dirname(filename), delete=False
        ) as fdesc:
            fdesc.write(utf8_data)
            tmp_filename = fdesc.name
            if not private:
                os.chmod(os.path.dirname(filename), 0o644)
        os.replace(tmp_filename, filename)
    except OSError as error:
        _LOGGER.exception("Saving file failed: %s", filename)
        raise PConnError(error) from error
    finally:
        if os.path.exists(tmp_filename):
            try:
                os.remove(tmp_filename)
            except OSError as err:
                # If we are cleaning up then something else went wrong, so
                # we should suppress likely follow-on errors in the cleanup
                _LOGGER.error(
                    "File replacement cleanup failed for %s while saving %s: %s",
                    tmp_filename,
                    filename,
                    err,
                )


def save_json(
    filename: str,
    data: list | dict,
    private: bool = False,
) -> None:
    """Save JSON data to a file."""
    json_data = _orjson_default_encoder(data)
    write_utf8_file(filename, json_data, private)
