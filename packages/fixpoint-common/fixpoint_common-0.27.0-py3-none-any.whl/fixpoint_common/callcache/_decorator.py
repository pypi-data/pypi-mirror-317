"""Decorators for caching functions."""

__all__ = [
    "async_cacheit",
    "cacheit",
    "get_async_func_return_type",
    "get_sync_func_return_type",
    "org_async_cacheit",
    "org_cacheit",
]

from functools import wraps
import inspect
from typing import Any, Callable, Optional, Type, cast

from fixpoint_common.constants import NO_AUTH_ORG_ID
from fixpoint_common.types.basic import Params, Ret, AsyncFunc
from fixpoint_common.cache import CacheMode
from ._shared import (
    CallCache,
    CallCacheKind,
    CacheResult,
    serialize_args,
    logger,
    format_cache_key,
)


_GLOBAL_RUN_ID = "__global__"


def cacheit(
    kind: CallCacheKind,
    kind_id: str,
    callcache: CallCache,
    cache_mode: CacheMode = "normal",
    run_id: str = _GLOBAL_RUN_ID,
    ttl_s: Optional[float] = None,
) -> Callable[[Callable[Params, Ret]], Callable[Params, Ret]]:
    """Decorate a sync function for call durability.

    Decorate a sync function for call durability, so that we store the results
    of calling a function. If the workflow fails and we recall the function, we
    can check if we already computed its results.
    """
    return org_cacheit(
        org_id=NO_AUTH_ORG_ID,
        kind=kind,
        kind_id=kind_id,
        callcache=callcache,
        cache_mode=cache_mode,
        run_id=run_id,
        ttl_s=ttl_s,
    )


def org_cacheit(
    org_id: str,
    kind: CallCacheKind,
    kind_id: str,
    callcache: CallCache,
    cache_mode: CacheMode = "normal",
    run_id: str = _GLOBAL_RUN_ID,
    ttl_s: Optional[float] = None,
) -> Callable[[Callable[Params, Ret]], Callable[Params, Ret]]:
    """Decorate a sync function for call durability.

    Decorate a sync function for call durability, so that we store the results
    of calling a function. If the workflow fails and we recall the function, we
    can check if we already computed its results.
    """

    def decorator(func: Callable[Params, Ret]) -> Callable[Params, Ret]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Ret:
            serialized = serialize_args(*args, **kwargs)

            cache_check = _check_cache(
                callcache=callcache,
                org_id=org_id,
                wrun_id=run_id,
                kind=kind,
                kind_id=kind_id,
                cache_mode=cache_mode,
                serialized_args=serialized,
                type_hint=get_sync_func_return_type(func),
            )
            match cache_check:
                case CacheResult(found=True, result=cache_res):
                    logger.debug(
                        f"Returning cache hit for {format_cache_key(kind, kind_id, serialized)}"
                    )
                    # we can cast this, because while `cache_res` is of type
                    # Optional[Ret], if `found is True`, then `cache_res` is
                    # actually of type `Ret`.
                    #
                    # We can't just do an `is None` check, because technically
                    # the result could be of type `None`.
                    return cast(Ret, cache_res)

            logger.debug(
                f"Running callcache function {format_cache_key(kind, kind_id, serialized)}"
            )
            res = func(*args, **kwargs)
            if cache_mode == "normal":
                callcache.store_result(
                    org_id=org_id,
                    run_id=run_id,
                    kind_id=kind_id,
                    serialized_args=serialized,
                    res=res,
                    ttl_s=ttl_s,
                )
            return res

        return wrapper

    return decorator


def async_cacheit(
    kind: CallCacheKind,
    kind_id: str,
    callcache: CallCache,
    cache_mode: CacheMode = "normal",
    run_id: str = _GLOBAL_RUN_ID,
    ttl_s: Optional[float] = None,
) -> Callable[[AsyncFunc[Params, Ret]], AsyncFunc[Params, Ret]]:
    """Decorate an async function for call durability.

    Decorate an async function for call durability, so that we store the results
    of calling a function. If the workflow fails and we recall the function, we
    can check if we already computed its results.
    """
    return org_async_cacheit(
        org_id=NO_AUTH_ORG_ID,
        kind=kind,
        kind_id=kind_id,
        callcache=callcache,
        cache_mode=cache_mode,
        run_id=run_id,
        ttl_s=ttl_s,
    )


def org_async_cacheit(
    org_id: str,
    kind: CallCacheKind,
    kind_id: str,
    callcache: CallCache,
    cache_mode: CacheMode = "normal",
    run_id: str = _GLOBAL_RUN_ID,
    ttl_s: Optional[float] = None,
) -> Callable[[AsyncFunc[Params, Ret]], AsyncFunc[Params, Ret]]:
    """Decorate an async function for call durability.

    Decorate an async function for call durability, so that we store the results
    of calling a function. If the workflow fails and we recall the function, we
    can check if we already computed its results.
    """

    def decorator(func: AsyncFunc[Params, Ret]) -> AsyncFunc[Params, Ret]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Ret:
            serialized = serialize_args(*args, **kwargs)

            cache_check = await _async_check_cache(
                callcache=callcache,
                org_id=org_id,
                wrun_id=run_id,
                kind=kind,
                kind_id=kind_id,
                cache_mode=cache_mode,
                serialized_args=serialized,
                type_hint=get_async_func_return_type(func),
            )
            match cache_check:
                case CacheResult(found=True, result=cache_res):
                    logger.debug(
                        f"Returning cache hit for {format_cache_key(kind, kind_id, serialized)}"
                    )
                    # we can cast this, because while `cache_res` is of type
                    # Optional[Ret], if `found is True`, then `cache_res` is
                    # actually of type `Ret`.
                    #
                    # We can't just do an `is None` check, because technically
                    # the result could be of type `None`.
                    return cast(Ret, cache_res)

            logger.debug(
                f"Running callcache function {format_cache_key(kind, kind_id, serialized)}"
            )
            res = await func(*args, **kwargs)
            if cache_mode == "normal":
                await callcache.async_store_result(
                    org_id=org_id,
                    run_id=run_id,
                    kind_id=kind_id,
                    serialized_args=serialized,
                    res=res,
                    ttl_s=ttl_s,
                )
            return res

        return wrapper

    return decorator


def get_async_func_return_type(func: AsyncFunc[Params, Ret]) -> Type[Ret]:
    """Get the return type of an async function"""
    sig = inspect.signature(func)
    return cast(Type[Ret], sig.return_annotation)


def get_sync_func_return_type(func: Callable[Params, Ret]) -> Type[Ret]:
    """Get the return type of an async function"""
    sig = inspect.signature(func)
    return cast(Type[Ret], sig.return_annotation)


def _check_cache(
    *,
    callcache: CallCache,
    org_id: str,
    wrun_id: str,
    kind: CallCacheKind,
    kind_id: str,
    cache_mode: CacheMode,
    serialized_args: str,
    type_hint: Type[Ret],
) -> CacheResult[Ret]:
    if cache_mode in ("skip_lookup", "skip_all"):
        logger.debug(
            f"Skipping cache lookup for {format_cache_key(kind, kind_id, serialized_args)}"
        )
        return CacheResult(found=False, result=None)
    return callcache.check_cache(
        org_id=org_id,
        run_id=wrun_id,
        kind_id=kind_id,
        serialized_args=serialized_args,
        type_hint=type_hint,
    )


async def _async_check_cache(
    *,
    callcache: CallCache,
    org_id: str,
    wrun_id: str,
    kind: CallCacheKind,
    kind_id: str,
    cache_mode: CacheMode,
    serialized_args: str,
    type_hint: Type[Ret],
) -> CacheResult[Ret]:
    if cache_mode in ("skip_lookup", "skip_all"):
        logger.debug(
            f"Skipping cache lookup for {format_cache_key(kind, kind_id, serialized_args)}"
        )
        return CacheResult(found=False, result=None)
    return await callcache.async_check_cache(
        org_id=org_id,
        run_id=wrun_id,
        kind_id=kind_id,
        serialized_args=serialized_args,
        type_hint=type_hint,
    )
