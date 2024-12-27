"""A human-in-the-loop client with all methods not implemented"""

__all__ = ["UnsupportedHumanInTheLoop"]

from pydantic import BaseModel

from fixpoint_common.types import HumanTaskEntry
from .human import HumanInTheLoop


class UnsupportedHumanInTheLoop(HumanInTheLoop):
    """Human-in-the-loop client that is not supported"""

    def send_task_entry(
        self,
        org_id: str,
        workflow_id: str,
        workflow_run_id: str,
        task_id: str,
        data: BaseModel,
    ) -> HumanTaskEntry:
        """Sends a task entry"""
        raise NotImplementedError("Unsupported")

    def get_task_entry(self, org_id: str, task_entry_id: str) -> HumanTaskEntry | None:
        """Retrieves a task"""
        raise NotImplementedError("Unsupported")
