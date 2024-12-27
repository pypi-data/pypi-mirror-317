"""The context for a workflow"""

import logging
from typing import Optional

from .workflow import Workflow, WorkflowRun


class WorkflowContext:
    """Context for a workflow.

    Holds all relevant context for a workflow. Pass this into every step
    function of your workflow.
    """

    workflow_run: WorkflowRun
    logger: logging.Logger

    def __init__(
        self,
        workflow_run: WorkflowRun,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.workflow_run = workflow_run
        self.logger = logger or self._setup_logger(workflow_run)

    def _setup_logger(self, workflow_run: WorkflowRun) -> logging.Logger:
        logger = logging.getLogger(f"fixpoint/workflows/runs/{workflow_run.id}")
        # We need to add this stream handler, because otherwise I think the
        # logger is using the handler from the default logger, which has a
        # log-level of "warning". This means that we do not print "info" logs.
        c_handler = logging.StreamHandler()
        logger.addHandler(c_handler)
        logger.setLevel(logging.INFO)
        return logger

    @classmethod
    def load_from_workflow_run(
        cls,
        org_id: str,
        workflow: Workflow,
        workflow_run_id: str,
    ) -> "WorkflowContext":
        """Load a workflow run's context from a workflow run id"""
        run = workflow.load_run(org_id=org_id, workflow_run_id=workflow_run_id)
        if not run:
            raise ValueError(f"Workflow run {workflow_run_id} not found")
        return cls(workflow_run=run)

    @property
    def wfrun(self) -> WorkflowRun:
        """The workflow run"""
        return self.workflow_run

    def clone(
        self, new_task: str | None = None, new_step: str | None = None
    ) -> "WorkflowContext":
        """Clones the workflow context"""
        # clone the workflow run
        new_workflow_run = self.workflow_run.clone(new_task=new_task, new_step=new_step)
        return self.__class__(
            workflow_run=new_workflow_run,
            logger=self.logger,
        )
