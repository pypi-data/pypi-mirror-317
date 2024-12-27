"""Values that are ignored by the durability callcache"""

from typing import Generic, TypeVar

T = TypeVar("T")


class CacheIgnored(Generic[T]):
    """Wrap a value to be ignored by the durability callcache

    Wrap a value to be ignored by the durability callcache for tasks and steps.
    """

    value: T

    def __init__(self, value: T):
        self.value = value
