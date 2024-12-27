"""Utilities for working with concurrency"""

__all__ = ["OptimisticTaskGroup"]

import asyncio


class OptimisticTaskGroup(asyncio.TaskGroup):
    """An asyncio TaskGroup that doesn't cancel other tasks if one fails.

    When we exit the context manager, we will still raise an exception with any
    failed tasks.
    """

    # Override this so failed tasks don't cancel each other
    def _abort(self) -> None:
        pass
