"""HTTP Utility functions."""

__all__ = ["route_url", "new_api_key_http_header"]

import os
from typing import Dict

from urllib.parse import urljoin


def route_url(base_url: str, *route_parts: str) -> str:
    """Join the base URL with the given route."""
    return urljoin(base_url, os.path.join(*route_parts))


def new_api_key_http_header(api_key: str) -> Dict[str, str]:
    """Create a new API key HTTP header."""
    return {"X-Api-Key": api_key}
