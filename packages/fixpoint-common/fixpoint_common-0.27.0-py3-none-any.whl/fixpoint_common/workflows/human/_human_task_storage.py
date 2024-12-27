"""Human task storage for workflows"""

__all__ = ["HumanTaskStorage"]

from typing import List, Optional, Protocol
from fixpoint_common.types import HumanTaskEntry, ListHumanTaskEntriesRequest


class HumanTaskStorage(Protocol):
    """Human task storage for workflows"""

    # pylint: disable=redefined-builtin
    def get(
        self,
        org_id: str,
        id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[HumanTaskEntry]:
        """Get the given human task"""

    async def async_get(
        self,
        org_id: str,
        id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[HumanTaskEntry]:
        """Get the given human task"""

    def create(self, org_id: str, task: HumanTaskEntry) -> None:
        """Create a new human task"""

    async def async_create(self, org_id: str, task: HumanTaskEntry) -> None:
        """Create a new human task"""

    def update(self, org_id: str, task: HumanTaskEntry) -> None:
        """Update an existing human task"""

    async def async_update(self, org_id: str, task: HumanTaskEntry) -> None:
        """Update an existing human task"""

    def list(
        self,
        org_id: str,
        req: ListHumanTaskEntriesRequest,
    ) -> List[HumanTaskEntry]:
        """List all human tasks

        Args:
            org_id: The organization ID.
            req: The query request for listing human task entries.


        Returns:
            A list of HumanTaskEntry objects matching the given criteria.
        """

    async def async_list(
        self,
        org_id: str,
        req: ListHumanTaskEntriesRequest,
    ) -> List[HumanTaskEntry]:
        """List all human tasks

        Args:
            org_id: The organization ID.
            req: The query request for listing human task entries.

        Returns:
            A list of HumanTaskEntry objects matching the given criteria.
        """
