"""The workflow context for structured workflows"""

import logging
from typing import Optional

from ..imperative import WorkflowContext as ImperativeWorkflowContext, WorkflowRun
from ._run_config import RunConfig


class WorkflowContext:
    """A context for a structured workflow

    A WorkflowContext tracks the current WorkflowRun, and it contains a few
    things:

    - The `workflow_run` itself, with which you can inspect the current node
      state (what task and step are we in?), store and search documents scoped to
      the workflow, and fill out structured forms scoped to the workflow.
    - A logger that is scoped to the lifetime of the `WorkflowRun`.
    - The `run_config`, that defines settings for the worflow run. You rarely
      need to access this.
    """

    run_config: RunConfig
    _imp_ctx: ImperativeWorkflowContext

    def __init__(
        self,
        run_config: RunConfig,
        workflow_run: WorkflowRun,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._imp_ctx = ImperativeWorkflowContext(
            workflow_run=workflow_run,
            logger=logger,
        )
        self.run_config = run_config

    @property
    def workflow_run(self) -> WorkflowRun:
        """The workflow run"""
        return self._imp_ctx.workflow_run

    @property
    def org_id(self) -> str:
        """The org id"""
        return self.workflow_run.org_id

    @property
    def workflow_id(self) -> str:
        """The workflow id"""
        return self.workflow_run.workflow_id

    @property
    def run_id(self) -> str:
        """The run id"""
        return self.workflow_run.id

    @property
    def run_attempt_id(self) -> str:
        """The run attempt id"""
        return self.workflow_run.attempt_id

    @property
    def logger(self) -> logging.Logger:
        """The workflow run context's logger"""
        return self._imp_ctx.logger

    def clone(
        self, new_task: str | None = None, new_step: str | None = None
    ) -> "WorkflowContext":
        """Clones the workflow context"""

        # We need to override this metod from the child class because we have
        # different init parameters.

        # clone the workflow run
        new_workflow_run = self.workflow_run.clone(new_task=new_task, new_step=new_step)
        return self.__class__(
            workflow_run=new_workflow_run,
            logger=self.logger,
            run_config=self.run_config,
        )
