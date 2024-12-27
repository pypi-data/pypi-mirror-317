"""Form storage for workflows"""

__all__ = [
    "FormStorage",
]

from typing import List, Optional, Protocol

from pydantic import BaseModel

from fixpoint_common.types import Form


class FormStorage(Protocol):
    """Form storage for workflows"""

    def get(
        self, org_id: str, id: str  # pylint: disable=redefined-builtin
    ) -> Optional[Form[BaseModel]]:
        """Get the given Form"""

    def create(self, org_id: str, form: Form[BaseModel]) -> None:
        """Create a new Form"""

    def update(self, org_id: str, form: Form[BaseModel]) -> None:
        """Update an existing Form"""

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> List[Form[BaseModel]]:
        """List all Forms

        If path is provided, list Forms in the given path.
        """
