"""Module for caching task and step executions."""

__all__ = [
    "CacheResult",
    "CallCache",
    "CallCacheKind",
    "deserialize_json_val",
    "format_cache_key",
    "JSONEncoder",
    "logger",
    "serialize_args",
    "serialize_func_cache_key",
    "serialize_step_cache_key",
    "serialize_task_cache_key",
    "T",
]

import dataclasses
from dataclasses import is_dataclass
from enum import Enum
import json
from typing import Any, Generic, Optional, Protocol, Type, TypeVar

from pydantic import BaseModel

from fixpoint_common.logging import callcache_logger as logger
from ._cache_ignored import CacheIgnored
from ._cache_keyed import CacheKeyed
from ._converter import value_to_type


T = TypeVar("T")


class CallCacheKind(Enum):
    """Kind of call cache to use"""

    TASK = "task"
    STEP = "step"
    FUNC = "func"


@dataclasses.dataclass
class CacheResult(Generic[T]):
    """The result of a cache check

    The result of a cache check. If there is a cache hit, `found is True`, and
    `result` is of type `T`. If there is a cache miss, `found is False`, and
    `result` is `None`.

    Note that `T` can also be `None` even if there is a cache hit, so don't rely
    on checking `cache_result.result is None`. Check `cache_result.found`.
    """

    found: bool
    result: Optional[T]


class CallCache(Protocol):
    """Protocol for a call cache for tasks or steps"""

    cache_kind: CallCacheKind

    def check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""

    def store_result(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        res: Any,
        ttl_s: Optional[float] = None,
    ) -> None:
        """Store the result of a task or step call"""

    async def async_check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""

    async def async_store_result(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        res: Any,
        ttl_s: Optional[float] = None,
    ) -> None:
        """Store the result of a task or step call"""


class JSONEncoder(json.JSONEncoder):
    """Encoder to serialize objects to JSON"""

    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.model_dump()
        if is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        return super().default(o)


def serialize_args(*args: Any, **kwargs: Any) -> str:
    """Serialize arbitrary arguments and keyword arguments to a string"""
    cleaned_args = [
        _transform_arg(arg) for arg in args if not isinstance(arg, CacheIgnored)
    ]
    cleaned_kwargs = {
        key: _transform_arg(val)
        for key, val in kwargs.items()
        if not isinstance(val, CacheIgnored)
    }
    return default_json_dumps({"args": cleaned_args, "kwargs": cleaned_kwargs})


def _transform_arg(arg: Any) -> Any:
    if isinstance(arg, CacheKeyed):
        return arg.key
    return arg


def serialize_step_cache_key(
    *, org_id: str, run_id: str, step_id: str, args: str
) -> str:
    """Serialize a step cache key to a string"""
    return default_json_dumps(
        {"org_id": org_id, "run_id": run_id, "step_id": step_id, "args": args}
    )


def serialize_task_cache_key(
    *, org_id: str, run_id: str, task_id: str, args: str
) -> str:
    """Serialize a task cache key to a string"""
    return default_json_dumps(
        {"org_id": org_id, "run_id": run_id, "task_id": task_id, "args": args}
    )


def serialize_func_cache_key(
    *, org_id: str, run_id: str, func_name: str, args: str
) -> str:
    """Serialize a func cache key to a string"""
    return default_json_dumps(
        {"org_id": org_id, "run_id": run_id, "func_name": func_name, "args": args}
    )


def default_json_dumps(obj: Any) -> str:
    """Default serialization of an object to JSON"""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), cls=JSONEncoder)


def deserialize_json_val(
    value_str: str,
    type_hint: Optional[Type[Any]] = None,
) -> Any:
    """Deserialize a JSON value to a type based on the type hint"""
    deserialized = json.loads(value_str)
    if type_hint is None:
        return deserialized
    return value_to_type(hint=type_hint, value=deserialized)


def format_cache_key(
    kind: CallCacheKind, kind_id: str, serialized_args: str, max_args_size: int = 100
) -> str:
    """Format a cache key into a readable string"""
    if len(serialized_args) > max_args_size:
        args = serialized_args[:max_args_size] + "..."
    else:
        args = serialized_args
    return f"{kind.value}:{kind_id} with key = {args}"
