"""Internal helpers for the structured workflow system"""

from functools import wraps, update_wrapper
import inspect
from typing import Any, Callable, Tuple

from fixpoint_common.types.basic import Params, Ret, AsyncFunc
from fixpoint_common.callcache import CallCache, CallCacheKind, org_async_cacheit
from fixpoint_common.cache import CacheMode
from ._context import WorkflowContext
from .errors import DefinitionError, InternalError
from ._errors import InternalExecutionError


def validate_func_has_context_arg(func: Callable[..., Any]) -> None:
    """Validate that a function has a WorkflowContext as its first argument

    If the function is a method, we expect the first argument to be "self" and
    the next argument to be a a WorkflowContext.
    """
    sig = inspect.signature(func)
    if len(sig.parameters) < 1:
        raise DefinitionError(
            "Function must take at least one argument of type WorkflowContext"
        )
    first_param = list(sig.parameters.values())[0]
    if first_param.name == "self":
        if len(sig.parameters) < 2:
            raise DefinitionError(
                "In class method: first non-self parameter must be of type WorkflowContext"
            )


def decorate_with_cache(
    kind: CallCacheKind, kind_id: str, cache_mode: CacheMode
) -> Callable[[AsyncFunc[Params, Ret]], AsyncFunc[Params, Ret]]:
    """Decorate a task or a step for call durability.

    Decorate a step or a task for call durability, so that we store the results
    of calling a task or a step. If the workflow fails and we recall the task or
    step, we can check if we already computed its results.
    """

    def decorator(func: AsyncFunc[Params, Ret]) -> AsyncFunc[Params, Ret]:
        validate_func_has_context_arg(func)

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Ret:
            ctx, ctx_pos = _pull_ctx_arg(*args)
            wrun_id = ctx.workflow_run.id
            org_id = ctx.workflow_run.org_id
            callcache = _get_callcache(ctx, kind)

            remaining_args = args[ctx_pos + 1 :]

            # This is the inner wrapper that does not have the ctx as an
            # argument. We need to remove the `ctx` argument before we use the
            # `org_async_cacheit` function because the `ctx` argument is supposed to
            # be ignored by the cache.
            async def inner_func(*inner_args: Any, **inner_kwargs: Any) -> Ret:
                return await func(ctx, *inner_args, **inner_kwargs)  # type: ignore[arg-type]

            # This is necessary to preserve the typing annotations for our
            # TypeVars. Otherwise, when the caching decorator tries to inspect
            # the return type to deserialize it, it only sees a generic TypeVar,
            # which it cannot make sense of.
            update_wrapper(inner_func, func)

            cached_func = org_async_cacheit(
                org_id, kind, kind_id, callcache, cache_mode, wrun_id
            )(inner_func)

            return await cached_func(*remaining_args, **kwargs)

        return wrapper

    return decorator


def _get_callcache(ctx: WorkflowContext, kind: CallCacheKind) -> CallCache:
    if kind == CallCacheKind.TASK:
        return ctx.run_config.call_cache.tasks
    elif kind == CallCacheKind.STEP:
        return ctx.run_config.call_cache.steps
    else:
        raise InternalError(f"Unknown call cache kind: {kind}")


def _pull_ctx_arg(*args: Any) -> Tuple[WorkflowContext, int]:
    """Return the WorkflowContext from function params, along with its position.

    Return the WorkflowContext argument and its position in the args, which will
    either be 0 or 1. If the function is a method, we can skip the first
    argument because it will be `self`.

    Raises a CallException if the WorkflowContext is not found.
    """
    if len(args) == 0:
        raise _new_workflow_context_expected_exc()
    if isinstance(args[0], WorkflowContext):
        return args[0], 0
    if len(args) <= 1:
        raise _new_workflow_context_expected_exc()
    if isinstance(args[1], WorkflowContext):
        return args[1], 1
    raise _new_workflow_context_expected_exc()


def _new_workflow_context_expected_exc() -> InternalExecutionError:
    return InternalExecutionError("Expected WorkflowContext as first argument")
