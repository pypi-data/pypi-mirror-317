"""Caching settings"""

__all__ = ["CacheMode"]

from typing import Literal

# Types of cache modes:
#
# - skip_lookup: Don't look up keys in the cache, but write results to the
#   cache.
# - skip_all: Don't look up the cache, and don't store the result.
# - normal: Look up the cache, and store the result if it's not in the cache.
CacheMode = Literal["skip_lookup", "skip_all", "normal"]
