"""In-memory call-cache"""

__all__ = ["StepInMemCallCache", "TaskInMemCallCache"]

from typing import Any, Dict, Optional, Type

from ._shared import (
    CallCache,
    CallCacheKind,
    CacheResult,
    serialize_step_cache_key,
    serialize_task_cache_key,
    T,
)


class StepInMemCallCache(CallCache):
    """An in-memory call-cache for steps"""

    cache_kind = CallCacheKind.STEP
    _cache: Dict[str, Any]

    def __init__(self) -> None:
        self._cache = {}

    def check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[T]:
        key = serialize_step_cache_key(
            org_id=org_id, run_id=run_id, step_id=kind_id, args=serialized_args
        )
        if key not in self._cache:
            return CacheResult[T](found=False, result=None)
        return CacheResult[T](found=True, result=self._cache[key])

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
        if ttl_s is not None:
            raise ValueError("ttl_s is not supported for in-memory call-cache")
        key = serialize_step_cache_key(
            org_id=org_id, run_id=run_id, step_id=kind_id, args=serialized_args
        )
        self._cache[key] = res

    async def async_check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[T]:
        # Because this is in-memory, async and sync are the same
        return self.check_cache(
            org_id=org_id,
            run_id=run_id,
            kind_id=kind_id,
            serialized_args=serialized_args,
            type_hint=type_hint,
        )

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
        if ttl_s is not None:
            raise ValueError("ttl_s is not supported for in-memory call-cache")
        # Because this is in-memory, async and sync are the same
        self.store_result(
            org_id=org_id,
            run_id=run_id,
            kind_id=kind_id,
            serialized_args=serialized_args,
            res=res,
        )


class TaskInMemCallCache(CallCache):
    """An in-memory call-cache for tasks"""

    cache_kind = CallCacheKind.TASK
    _cache: Dict[str, Any]

    def __init__(self) -> None:
        self._cache = {}

    def check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[T]:
        key = serialize_task_cache_key(
            org_id=org_id, run_id=run_id, task_id=kind_id, args=serialized_args
        )
        if key not in self._cache:
            return CacheResult[T](found=False, result=None)
        return CacheResult[T](found=True, result=self._cache[key])

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
        if ttl_s is not None:
            raise ValueError("ttl_s is not supported for in-memory call-cache")
        key = serialize_task_cache_key(
            org_id=org_id, run_id=run_id, task_id=kind_id, args=serialized_args
        )
        self._cache[key] = res

    async def async_check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[T]:
        # Because this is in-memory, async and sync are the same
        return self.check_cache(
            org_id=org_id,
            run_id=run_id,
            kind_id=kind_id,
            serialized_args=serialized_args,
            type_hint=type_hint,
        )

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
        if ttl_s is not None:
            raise ValueError("ttl_s is not supported for in-memory call-cache")
        # Because this is in-memory, async and sync are the same
        self.store_result(
            org_id=org_id,
            run_id=run_id,
            kind_id=kind_id,
            serialized_args=serialized_args,
            res=res,
        )
