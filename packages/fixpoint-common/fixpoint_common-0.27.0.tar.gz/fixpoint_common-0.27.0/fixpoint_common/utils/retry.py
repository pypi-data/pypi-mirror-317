"""Utilities for retrying operations"""

__all__ = ["async_retry", "sync_retry"]

import asyncio
import random
import time
from functools import wraps
from typing import Callable, Awaitable

from fixpoint_common.types.basic import AsyncFunc, Ret, Params


def async_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    jitter: float = 0.1,
    exception_handler: Callable[[Exception, int], Awaitable[bool]] | None = None,
) -> Callable[[AsyncFunc[Params, Ret]], AsyncFunc[Params, Ret]]:
    """
    Decorator for asynchronous retry with jitter and optional exception handling.

    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Base delay between retries in seconds.
        jitter: Maximum random jitter to add to the delay.
        exception_handler: Optional function to handle exceptions. Return True
            if we should re-raise the exception, aborting the retry. Return
            False if we should follow our normal retry logic. Arguments are the
            exception and the current retry count.

    Returns:
        A decorator function.
    """

    def decorator(func: AsyncFunc[Params, Ret]) -> AsyncFunc[Params, Ret]:
        @wraps(func)
        async def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> Ret:
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    if exception_handler:
                        should_abort = await exception_handler(e, attempt)
                        if should_abort:
                            raise

                    if attempt == max_retries:
                        raise

                    delay = base_delay * (2**attempt) + random.uniform(0, jitter)
                    await asyncio.sleep(delay)

            raise RuntimeError("This should never be reached")

        return wrapper

    return decorator


def sync_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    jitter: float = 0.1,
    exception_handler: Callable[[Exception, int], bool] | None = None,
) -> Callable[[Callable[Params, Ret]], Callable[Params, Ret]]:
    """
    Decorator for synchronous retry with jitter and optional exception handling.

    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Base delay between retries in seconds.
        jitter: Maximum random jitter to add to the delay.
        exception_handler: Optional function to handle exceptions. Return True
            if we should re-raise the exception, aborting the retry. Return
            False if we should follow our normal retry logic. Arguments are the
            exception and the current retry count.

    Returns:
        A decorator function.
    """

    def decorator(func: Callable[Params, Ret]) -> Callable[Params, Ret]:
        @wraps(func)
        def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> Ret:
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    if exception_handler:
                        should_abort = exception_handler(e, attempt)
                        if should_abort:
                            raise

                    if attempt == max_retries:
                        raise

                    delay = base_delay * (2**attempt) + random.uniform(0, jitter)
                    time.sleep(delay)

            raise RuntimeError("This should never be reached")

        return wrapper

    return decorator
