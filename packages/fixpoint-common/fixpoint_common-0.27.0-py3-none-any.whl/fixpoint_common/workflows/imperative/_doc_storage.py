"""Document storage for workflows"""

__all__ = ["DocStorage"]

from typing import List, Optional, Protocol
from fixpoint_common.constants import NULL_COL_ID
from fixpoint_common.types import Document


class DocStorage(Protocol):
    """Document storage for workflows"""

    # pylint: disable=redefined-builtin
    def get(
        self,
        org_id: str,
        id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[Document]:
        """Get the given document"""

    def create(self, org_id: str, document: Document) -> None:
        """Create a new document"""

    def update(self, org_id: str, document: Document) -> None:
        """Update an existing document"""

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        task: Optional[str] = None,
        step: Optional[str] = None,
    ) -> List[Document]:
        """List all documents

        If path is provided, list documents in the given path.
        """


def _fix_doc_ids(doc: Document) -> Document:
    doc = doc.model_copy(deep=True)
    if doc.workflow_id is None:
        doc.workflow_id = NULL_COL_ID
    if doc.workflow_run_id is None:
        doc.workflow_run_id = NULL_COL_ID
    return doc
