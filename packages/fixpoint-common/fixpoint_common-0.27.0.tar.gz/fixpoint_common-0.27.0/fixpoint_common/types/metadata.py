"""Metadata for an API resource"""

__all__ = ["Metadata"]

from typing import Annotated, Dict, Optional

from pydantic import BeforeValidator
from ._helpers import json_deserializer

Metadata = Annotated[Optional[Dict[str, str]], BeforeValidator(json_deserializer)]
