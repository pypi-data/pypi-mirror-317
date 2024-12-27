"""Types for the callcache"""

__all__ = [
    "CacheEntry",
    "CreateCallcacheEntryRequest",
    "GetCallcacheEntryRequest",
]

from typing import Optional

from pydantic import BaseModel, Field


class CacheEntry(BaseModel):
    """The result of a callcache lookup"""

    found: bool = Field(description="Whether the cache was found")
    cache_key: str = Field(description="The cache key")
    result: Optional[str] = Field(
        description="The cached value if found, as a JSON string"
    )


class CreateCallcacheEntryRequest(BaseModel):
    """The request to create a callcache entry"""

    cache_key: str = Field(
        description="The cache key (normally the serialized args of the function we are caching)"
    )
    result: str = Field(description="The result to cache. Must be JSON-serializable.")


class GetCallcacheEntryRequest(BaseModel):
    """A request to get a cache entry"""

    cache_key: str = Field(description="The cache key to get")
