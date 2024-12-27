"""Human in the loop functionality"""

__all__ = ["HumanInTheLoop"]

from typing import Protocol

from pydantic import BaseModel

from fixpoint_common.types.human import HumanTaskEntry


class HumanInTheLoop(Protocol):
    """Human-in-the-loop client"""

    def send_task_entry(
        self,
        org_id: str,
        workflow_id: str,
        workflow_run_id: str,
        task_id: str,
        data: BaseModel,
    ) -> HumanTaskEntry:
        """Sends a task entry"""

    def get_task_entry(self, org_id: str, task_entry_id: str) -> HumanTaskEntry | None:
        """Retrieves a task"""
