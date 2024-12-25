"""Helper methods for Gallagher plugins."""

import json
from typing import Any


def format_stream_message(event: str, data: Any) -> str:
    """Format stream message."""
    try:
        return f"event: {event}\ndata: {json.dumps(data)}\n\n"
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON: {data}")
