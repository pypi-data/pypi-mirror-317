"""Structured workflows: task definitions and task entrypoints

In a structured workflow, a task is a section of a workflow. Its state is
checkpointed, so if the task fails you can resume without losing computed work.
In a workflow, agents are able to recall memories, documents, and forms from
past or current tasks within the workflow.
"""

from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
)

from fixpoint_common.cache import CacheMode
from fixpoint_common.callcache import CallCacheKind
from fixpoint_common.types.basic import AsyncFunc, Params, Ret
from ..constants import STEP_MAIN_ID
from .. import NodeStatus
from ._context import WorkflowContext
from .errors import DefinitionError
from ._helpers import (
    validate_func_has_context_arg,
    decorate_with_cache,
)


T = TypeVar("T")
C = TypeVar("C")


class TaskFixp:
    """The internal Fixpoint attribute for a task function"""

    id: str

    def __init__(self, id: str):  # pylint: disable=redefined-builtin
        self.id = id


def task(
    id: str,  # pylint: disable=redefined-builtin
    cache_mode: CacheMode = "normal",
) -> Callable[[AsyncFunc[Params, Ret]], AsyncFunc[Params, Ret]]:
    """Decorate a function to mark it as a task definition

    A task definition is a function that represents a section (task) in a
    workflow. The function must have at least one argument, which is the
    WorkflowContext.

    An example:

    ```
    @structured.task(id="my-task")
    def my_task(ctx: WorkflowContext, args: Dict[str, Any]) -> None:
        ...
    ```
    """

    def decorator(func: AsyncFunc[Params, Ret]) -> AsyncFunc[Params, Ret]:
        # pylint: disable=protected-access
        func.__fixp = TaskFixp(id)  # type: ignore[attr-defined]

        validate_func_has_context_arg(func)

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Ret:
            wrapped_func = decorate_with_cache(CallCacheKind.TASK, id, cache_mode)(func)
            result = await wrapped_func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def get_task_fixp(fn: Callable[..., Any]) -> Optional[TaskFixp]:
    """Get the internal task Fixpoint attribute for a function"""
    if not callable(fn):
        return None
    attr = getattr(fn, "__fixp", None)
    if isinstance(attr, TaskFixp):
        return attr
    return None


async def call_task(
    ctx: WorkflowContext,
    fn: AsyncFunc[Params, Ret],
    args: Optional[List[Any] | tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
) -> Ret:
    """Execute a task in a workflow.

    You must call `call_task` from within a structured workflow definition or a
    structured task definition. ie from a class decorated with
    `@structured.workflow(...)` or with `@structured.task(...)`.

    A more complete example:

    ```
    @structured.workflow(id="my-workflow")
    class MyWorkflow:
        @structured.workflow_entrypoint()
        def main(self, ctx: WorkflowContext, args: Dict[str, Any]) -> None:
            ####
            # this is the `call_task` invocation
            structured.call_task(ctx, my_task, args[{"somevalue": "foobar"}])

    @structured.task(id="my-task")
    def my_task(ctx: WorkflowContext, args: Dict[str, Any]) -> None:
        ...
    ```
    """
    args = args or []
    kwargs = kwargs or {}

    task_fixp = get_task_fixp(fn)
    if not task_fixp:
        raise DefinitionError(f"Task {fn.__name__} is not a valid task definition")

    task_handle = ctx.workflow_run.spawn_task(task_fixp.id)
    new_ctx = ctx.clone(new_task=task_fixp.id, new_step=STEP_MAIN_ID)
    try:
        ret = await fn(new_ctx, *args, **kwargs)  # type: ignore[arg-type]
    except:
        task_handle.close(NodeStatus.FAILED)
        raise
    else:
        task_handle.close(NodeStatus.COMPLETED)
    return ret
