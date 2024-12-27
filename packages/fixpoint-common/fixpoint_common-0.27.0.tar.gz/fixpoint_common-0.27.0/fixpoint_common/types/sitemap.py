"""
Types for creating and using site maps.
"""

__all__ = ["CreateSitemapRequest", "Sitemap"]

from typing import List

from pydantic import BaseModel


from .sources import WebpageSource
from ._shared import BaseRequest


class CreateSitemapRequest(BaseRequest):
    """Request to create a site map."""

    source: WebpageSource


class Sitemap(BaseModel):
    """A site map result."""

    source: WebpageSource
    urls: List[str]
