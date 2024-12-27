"""Shared types for Fixpoint requests."""

__all__ = ["BaseRequest"]

from pydantic import BaseModel

from .workflow import WorkflowRunId


class BaseRequest(BaseModel):
    """Base request class that all research requests must inherit from."""

    run_id: WorkflowRunId = None
