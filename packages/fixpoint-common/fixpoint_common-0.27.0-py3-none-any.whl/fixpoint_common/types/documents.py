"""A document is a set of text and metadata."""

__all__ = ["Document", "CreateDocumentRequest", "ListDocumentsResponse"]

from typing import Dict, Any, Optional, List

from pydantic import BaseModel, Field, computed_field

from fixpoint_common.constants import TASK_MAIN_ID, STEP_MAIN_ID
from .list_api import ListResponse
from .version import Version


class _BaseDocument(BaseModel):
    id: str = Field(
        description=("Must be unique within the workflow the document exists in."),
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata for document"
    )

    path: str = Field(
        default="/", description="The path to the document in the workflow"
    )

    versions: List[Version] = Field(
        default=[], description="The versions of the document"
    )

    contents: str = Field(description="The contents of the document")
    media_type: str = Field(
        description="The media type (MIME type) of the document", default="text/plain"
    )

    workflow_id: Optional[str] = Field(description="The workflow id", default=None)
    workflow_run_id: Optional[str] = Field(
        description="The workflow run id", default=None
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def task(self) -> str:
        """The task the document exists in"""
        # If path is empty or an empty string, return the main task, or doesn't start with /
        if not self.path or self.path == "/" or not self.path.startswith("/"):
            return TASK_MAIN_ID

        # Otherwise split the path on "/" and return the first part
        parts = self.path.split("/")
        if len(parts) == 1:
            return TASK_MAIN_ID
        return parts[1]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def step(self) -> str:
        """The step the document exists in"""
        # If path is empty or an empty string, return the main step, or doesn't start with /
        path = self.path.strip()
        if not path or path in ["/", "task", "/task", "task/", "/task/"]:
            return STEP_MAIN_ID

        parts = self.path.split("/")
        if len(parts) < 3:
            return STEP_MAIN_ID
        return parts[2]


class CreateDocumentRequest(_BaseDocument):
    """Request object for creating a document"""


class Document(_BaseDocument):
    """A document is a collection of text and metadata."""


class ListDocumentsResponse(ListResponse[Document]):
    """
    The response from listing documents
    """

    data: List[Document] = Field(description="The list of documents")
