"""Caller for task and step functions"""

from typing import Any, Dict, List, Optional

from fixpoint_common.types.basic import AsyncFunc, Params, Ret
from ._context import WorkflowContext
from .errors import DefinitionError
from ._task import get_task_fixp, call_task
from ._step import get_step_fixp, call_step


async def call(
    ctx: WorkflowContext,
    fn: AsyncFunc[Params, Ret],
    args: Optional[List[Any] | tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
) -> Ret:
    """Calls a task or a step function"""
    if get_task_fixp(fn):
        return await call_task(ctx, fn, args, kwargs)
    elif get_step_fixp(fn):
        return await call_step(ctx, fn, args, kwargs)
    else:
        raise DefinitionError(f"Function {fn} is not a task or a step")
