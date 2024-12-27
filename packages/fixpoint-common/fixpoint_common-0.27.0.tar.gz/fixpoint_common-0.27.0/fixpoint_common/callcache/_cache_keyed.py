"""Wrap a value with a key for the durability callcache"""

__all__ = ["CacheKeyed"]

from typing import Generic, TypeVar

T = TypeVar("T")


class CacheKeyed(Generic[T]):
    """Wrap a value with a key for the durability callcache

    Wrap a value with a key to be used by the durability callcache for tasks and steps.
    The key determines how the value is cached.
    """

    value: T
    key: str

    def __init__(self, value: T, key: str):
        self.value = value
        self.key = key
