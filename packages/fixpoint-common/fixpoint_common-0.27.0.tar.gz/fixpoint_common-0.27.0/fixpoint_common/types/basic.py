"""Types for the Fixpoint package"""

__all__ = ["AsyncFunc", "AwaitableRet", "Params", "Ret_co", "Ret", "T"]

from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    ParamSpec,
    TypeVar,
)

from pydantic import BaseModel


T = TypeVar("T")
BM = TypeVar("BM", bound=BaseModel)
Params = ParamSpec("Params")
Ret = TypeVar("Ret")
Ret_co = TypeVar("Ret_co", covariant=True)
AwaitableRet = TypeVar("AwaitableRet", bound=Awaitable[Any])
AsyncFunc = Callable[Params, Coroutine[Any, Any, Ret]]
