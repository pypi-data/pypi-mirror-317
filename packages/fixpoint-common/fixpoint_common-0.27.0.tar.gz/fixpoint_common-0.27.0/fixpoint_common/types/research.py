"""Definitions for Research (Records, Fields)"""

__all__ = [
    "CreateResearchRecordRequest",
    "ListResearchRecordsRequest",
    "ListResearchRecordsResponse",
    "new_research_record_id",
    "ResearchField",
    "ResearchRecord",
    "SourceType",
    "CreateResearchDocumentRequest",
    "UpdateResearchDocumentRequest",
    "ListResearchDocumentsRequest",
    "ListResearchDocumentsResponse",
    "ResearchDocument",
]

import datetime
from typing import Any, Annotated, List, Optional, Type, TypeVar, Literal, Union

from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    BeforeValidator,
    AfterValidator,
    PlainSerializer,
)

from fixpoint_common.types.json_extraction import JsonSchemaExtraction
from fixpoint_common.utils.ids import make_resource_uuid
from ._helpers import json_deserializer, dt_to_utc
from .citations import Citation
from .metadata import Metadata
from .list_api import ListResponse
from .workflow import NodeStatus


BM = TypeVar("BM", bound=BaseModel)


class EditableConfig(BaseModel):
    """
    Configuration for whether a task entry field is editable.
    """

    is_editable: bool = Field(description="Whether the field is editable", default=True)
    is_required: bool = Field(
        description="Whether the field is required", default=False
    )
    human_contents: Optional[str] = Field(
        description="The human contents", default=None
    )


AiNotFound = Literal["not_found", "found", "not_applicable"]


class ResearchField(BaseModel):
    """
    A field in a research record (aka a column in a table)
    """

    id: str = Field(description="The field id")
    display_name: Optional[str] = Field(description="The display name", default=None)
    description: Optional[str] = Field(description="The description", default=None)
    ai_explanation: Optional[str] = Field(
        description="The explanation of how the AI came up with the contents",
        default=None,
    )
    ai_not_found: AiNotFound = Field(
        description="Whether the AI could produce the research record"
    )
    media_type: Optional[str] = Field(
        description="The media type of the contents. Defaults to 'text/plain' if not set.",
        default=None,
    )
    contents: Optional[Any] = Field(description="The contents", default=None)
    editable_config: EditableConfig = Field(
        description="The editable config",
        default_factory=EditableConfig,
    )
    citations: List[Citation] = Field(
        description="The citations for where the field contents came from",
        default_factory=list,
    )


def new_research_record_id() -> str:
    """Create a new research record id"""
    return make_resource_uuid("rrec")


def new_research_document_id() -> str:
    """Create a new research document id"""
    return make_resource_uuid("rdoc")


def _uppercase_validator(v: Any) -> Optional[Any]:
    if v is None:
        return None
    if isinstance(v, str):
        return v.upper()
    return v


def _serialize_status(v: Optional[NodeStatus]) -> Optional[str]:
    if v is None:
        return None
    return v.value


Status = Annotated[
    Optional[NodeStatus],
    BeforeValidator(_uppercase_validator),
    PlainSerializer(_serialize_status, return_type=Optional[str]),
]

SourceType = Literal["website_page", "url_crawl", "text_file", "batch_text_file"]


class _ResearchRecordBase(BaseModel):
    research_document_id: str = Field(
        description="The research document ID this record belongs to"
    )
    source: str = Field(
        description="The source of the research record (a website, a search query, etc.)"
    )
    source_type: SourceType = Field(
        description="The type of source (e.g. a 'website_page', 'url_crawl', 'text_file', etc.)"
    )
    workflow_run_id: str = Field(description="The workflow run id")
    workflow_source_node: Optional[str] = Field(
        description="Workflow node that created the task entry", default=None
    )

    status: Status = Field(
        description="The status of the task entry",
        default=NodeStatus.SUSPENDED,
    )

    fields: Annotated[
        List[ResearchField],
        BeforeValidator(json_deserializer),
        Field(
            description=(
                "The fields (aka columns) of the research record, which can be "
                "informational or editable by humans"
            )
        ),
    ]

    # We allow the metadata to be a string, because sometimes when we load this
    # data back in from a storage layer (DB, filesystem, etc.) it comes as a
    # string.
    metadata: Metadata = Field(default=None, description="Metadata for document")

    @classmethod
    def _pydantic_model_to_research_fields(
        cls, model: BaseModel
    ) -> List[ResearchField]:
        """Converts a pydantic model into a list of research fields"""
        research_fields = []
        for field_name, field_info in model.model_fields.items():
            field_value = getattr(model, field_name)
            ef = ResearchField(
                id=field_name,
                ai_not_found="not_applicable",
                # TODO(jakub): Perhaps making display_name prettier is the solution?
                display_name=None,
                description=field_info.description,
                contents=field_value,
            )
            research_fields.append(ef)

        return research_fields


class CreateResearchRecordRequest(_ResearchRecordBase):
    """
    Request object for creating a research record.
    """

    # We must define this class method on each class because it returns a class
    # instance that is not the base class.
    @classmethod
    def from_pydantic_model(
        cls,
        *,
        research_document_id: str,
        source: str,
        source_type: Literal["website_page"],
        workflow_run_id: str,
        model: BaseModel,
        status: NodeStatus = NodeStatus.SUSPENDED,
    ) -> "CreateResearchRecordRequest":
        """Creates a research record from a pydantic model"""
        research_fields = cls._pydantic_model_to_research_fields(model)
        return cls(
            research_document_id=research_document_id,
            source=source,
            source_type=source_type,
            workflow_run_id=workflow_run_id,
            fields=research_fields,
            status=status,
        )


class ResearchRecord(_ResearchRecordBase):
    """
    A research record.
    """

    id: str = Field(
        description="The system-generated id of the research record",
        default_factory=new_research_record_id,
    )

    org_id: str = Field(description="The organization id owning the research record")

    created_at: Annotated[datetime.datetime, AfterValidator(dt_to_utc)] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The created at timestamp",
    )
    updated_at: Annotated[datetime.datetime, AfterValidator(dt_to_utc)] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The updated at timestamp",
    )

    # These are not in the `_ResearchRecordBase` because we do not want the user
    # to be able to configure in a `CreateResearchRecordRequest`. For example,
    # we calculate usage and billing based on the `cost` parameter.
    sub_json_extractions: List[JsonSchemaExtraction] = Field(
        description="The sub-extractions that resulted in this extraction.",
        default_factory=list,
        exclude=True,
    )
    ai_model: Optional[str] = Field(
        description="The AI model used to generate this research record",
        default=None,
    )
    cost: Optional[Union[float, int]] = Field(
        description="The cost associated with generating this research record",
        default=None,
    )

    @field_serializer("created_at", "updated_at")
    def _serialize_datetime(self, v: datetime.datetime, _info: Any) -> str:
        vnew = v.replace(tzinfo=datetime.timezone.utc)
        return vnew.isoformat()

    # We must define this class method on each class because it returns a class
    # instance that is not the base class.
    @classmethod
    def from_pydantic_model(
        cls,
        *,
        id: str,  # pylint: disable=redefined-builtin
        org_id: str,
        research_document_id: str,
        source: str,
        source_type: Literal["website_page"],
        workflow_run_id: str,
        model: BaseModel,
        status: NodeStatus = NodeStatus.SUSPENDED,
        ai_model: Optional[str] = None,
        cost: Optional[Union[float, int]] = None,
        sub_json_extractions: List[JsonSchemaExtraction] = Field(default_factory=list),
    ) -> "ResearchRecord":
        """Creates a research record from a pydantic model"""
        research_fields = cls._pydantic_model_to_research_fields(model)
        return cls(
            id=id,
            org_id=org_id,
            research_document_id=research_document_id,
            source=source,
            source_type=source_type,
            workflow_run_id=workflow_run_id,
            fields=research_fields,
            status=status,
            ai_model=ai_model,
            cost=cost,
            sub_json_extractions=sub_json_extractions,
        )

    def to_pydantic_model(self, model_cls: Type[BM]) -> BM:
        """Converts a research record into an instance of the type of the original model"""
        new_data = {
            item.id: item.editable_config.human_contents or item.contents
            # cast to a list so pylint doesn't yell
            for item in list(self.fields)
        }

        return model_cls(**new_data)


class ListResearchRecordsRequest(BaseModel):
    """Query parameters for listing research records."""

    research_document_id: str = Field(
        description=("Filter to research records for a specific research document."),
    )
    workflow_run_id: Optional[str] = Field(
        default=None, description="Filter by workflow run ID of the research record"
    )
    sampling_size: Optional[int] = Field(
        default=None, description="The number of research records to randomly sample"
    )

    metadata: Optional[Metadata] = Field(
        default=None, description="Filter by metadata of the research record"
    )

    status: Optional[Status] = Field(
        default=None, description="Filter by status of the research record"
    )


class ListResearchRecordsResponse(ListResponse[ResearchRecord]):
    """
    The response from listing research records
    """

    data: List[ResearchRecord] = Field(description="The list of research records")


class _ResearchDocumentBase(BaseModel):
    """Base class for research document-related classes"""

    name: Optional[str] = Field(description="The name of the research document")
    description: Optional[str] = Field(
        description="The description of the research document"
    )


class CreateResearchDocumentRequest(_ResearchDocumentBase):
    """Request object for creating a new research document"""

    id: Optional[str] = None


class ResearchDocument(_ResearchDocumentBase):
    """A collection of research records"""

    id: str = Field(
        description="The system-generated id of the research document",
        default_factory=new_research_document_id,
    )
    created_at: Annotated[datetime.datetime, AfterValidator(dt_to_utc)] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The created at timestamp",
    )
    updated_at: Annotated[datetime.datetime, AfterValidator(dt_to_utc)] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The updated at timestamp",
    )


class ListResearchDocumentsRequest(BaseModel):
    """Query parameters for listing research documents."""


class ListResearchDocumentsResponse(ListResponse[ResearchDocument]):
    """
    The response from listing research records
    """

    data: List[ResearchDocument] = Field(description="The list of research documents")


class UpdateResearchDocumentRequest(_ResearchDocumentBase):
    """Request object for updating an existing research document"""

    name: Optional[str] = Field(
        default=None, description="The updated name of the research document"
    )
    description: Optional[str] = Field(
        default=None, description="The updated description of the research document"
    )
