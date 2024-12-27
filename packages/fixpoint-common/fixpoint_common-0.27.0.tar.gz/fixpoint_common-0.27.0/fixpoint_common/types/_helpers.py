"""Helper functions for types and Pydantic models"""

__all__ = ["json_deserializer", "dt_to_utc"]

import datetime
import json
from typing import Any, Optional


def json_deserializer(v: Any) -> Optional[Any]:
    """Pydantic deserializer to deserialize a JSON string to a Python object"""
    if v is None:
        return None
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError("field is not a valid JSON string") from e
    return v


def dt_to_utc(v: datetime.datetime) -> datetime.datetime:
    """Convert a datetime to UTC"""
    return v.replace(tzinfo=datetime.timezone.utc)
