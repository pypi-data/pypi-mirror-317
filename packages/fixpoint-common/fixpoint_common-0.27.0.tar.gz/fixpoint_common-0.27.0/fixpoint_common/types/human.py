"""Definitions for human in the loop tasks"""

__all__ = [
    "CreateHumanTaskEntryRequest",
    "EditableConfig",
    "EntryField",
    "HumanTaskEntry",
    "ListHumanTaskEntriesRequest",
    "ListHumanTaskEntriesResponse",
]

import datetime
import json
from typing import Any, Annotated, Dict, List, Optional, Type, TypeVar

from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    BeforeValidator,
    AfterValidator,
    PlainSerializer,
)

from fixpoint_common.utils.ids import make_resource_uuid
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


class EntryField(BaseModel):
    """
    A field in a task entry that can either be editable by a human or
    informational.
    """

    id: str = Field(description="The field id")
    display_name: Optional[str] = Field(description="The display name", default=None)
    description: Optional[str] = Field(description="The description", default=None)
    contents: Optional[Any] = Field(description="The contents", default=None)
    editable_config: EditableConfig = Field(
        description="The editable config",
        default_factory=EditableConfig,
    )


def _new_task_entry_id() -> str:
    """Create a new workflow run id"""
    return make_resource_uuid("ht")


def _json_deserializer(v: Any) -> Optional[Any]:
    if v is None:
        return None
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError("field is not a valid JSON string") from e
    return v


def _uppercase_validator(v: Any) -> Optional[Any]:
    if v is None:
        return None
    if isinstance(v, str):
        return v.upper()
    return v


Metadata = Annotated[Optional[Dict[str, str]], BeforeValidator(_json_deserializer)]


def _serialize_status(v: Optional[NodeStatus]) -> Optional[str]:
    if v is None:
        return None
    return v.value


Status = Annotated[
    Optional[NodeStatus],
    BeforeValidator(_uppercase_validator),
    PlainSerializer(_serialize_status, return_type=Optional[str]),
]


class _HumanTaskEntryBase(BaseModel):
    task_id: str = Field(
        description="The task id (aka the task entry is an instance of this task definition)"
    )
    workflow_id: str = Field(description="The workflow id")
    workflow_run_id: str = Field(description="The workflow run id")
    source_node: Optional[str] = Field(
        description="Node that created the task entry", default=None
    )

    status: Status = Field(
        description="The status of the task entry",
        default=NodeStatus.SUSPENDED,
    )

    entry_fields: Annotated[List[EntryField], BeforeValidator(_json_deserializer)] = (
        Field(
            description=(
                "The fields of the task entry, which can be informational or "
                "editable by humans"
            )
        )
    )

    # We allow the metadata to be a string, because sometimes when we load this
    # data back in from a storage layer (DB, filesystem, etc.) it comes as a
    # string.
    metadata: Metadata = Field(default=None, description="Metadata for document")

    @classmethod
    def _pydantic_model_to_entry_fields(cls, model: BaseModel) -> List[EntryField]:
        """Converts a pydantic model into a list of entry fields"""
        entry_fields = []
        for field_name, field_info in model.model_fields.items():
            field_value = getattr(model, field_name)
            ef = EntryField(
                id=field_name,
                # TODO(jakub): Perhaps making display_name prettier is the solution?
                display_name=None,
                description=field_info.description,
                contents=field_value,
            )
            entry_fields.append(ef)

        return entry_fields


class CreateHumanTaskEntryRequest(_HumanTaskEntryBase):
    """
    Request object for creating a human task entry.
    """

    # We must define this class method on each class because it returns a class
    # instance that is not the base class.
    @classmethod
    def from_pydantic_model(
        cls,
        *,
        task_id: str,
        workflow_id: str,
        workflow_run_id: str,
        model: BaseModel,
        status: NodeStatus = NodeStatus.SUSPENDED,
    ) -> "CreateHumanTaskEntryRequest":
        """Creates a human task entry from a pydantic model"""
        entry_fields = cls._pydantic_model_to_entry_fields(model)
        return cls(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            entry_fields=entry_fields,
            status=status,
        )


def _dt_to_utc(v: datetime.datetime) -> datetime.datetime:
    """Convert a datetime to UTC"""
    return v.replace(tzinfo=datetime.timezone.utc)


class HumanTaskEntry(_HumanTaskEntryBase):
    """
    A task entry that a human can complete.
    """

    id: str = Field(
        description="The id of task entry", default_factory=_new_task_entry_id
    )

    created_at: Annotated[datetime.datetime, AfterValidator(_dt_to_utc)] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The created at timestamp",
    )
    updated_at: Annotated[datetime.datetime, AfterValidator(_dt_to_utc)] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The updated at timestamp",
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
        task_id: str,
        workflow_id: str,
        workflow_run_id: str,
        model: BaseModel,
        status: NodeStatus = NodeStatus.SUSPENDED,
    ) -> "HumanTaskEntry":
        """Creates a human task entry from a pydantic model"""
        entry_fields = cls._pydantic_model_to_entry_fields(model)
        return cls(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            entry_fields=entry_fields,
            status=status,
        )

    def to_pydantic_model(self, model_cls: Type[BM]) -> BM:
        """Converts a human task into an instance of the type of the original model"""
        new_data = {
            item.id: item.editable_config.human_contents or item.contents
            # cast to a list so pylint doesn't yell
            for item in list(self.entry_fields)
        }

        return model_cls(**new_data)


class ListHumanTaskEntriesRequest(BaseModel):
    """Query parameters for listing human task entries."""

    task_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter the task ID that the task entry belongs to "
            "(this is a way of grouping task entries that are similar)"
        ),
    )
    workflow_id: Optional[str] = Field(
        default=None, description="Filter by workflow ID of the task entry"
    )
    workflow_run_id: Optional[str] = Field(
        default=None, description="Filter by workflow run ID of the task entry"
    )
    sampling_size: Optional[int] = Field(
        default=None, description="The number of task entries to randomly sample"
    )

    metadata: Metadata = Field(
        default=None, description="Filter by metadata of the task entry"
    )

    status: Optional[Status] = Field(
        default=None, description="Filter by status of the task entry"
    )


class ListHumanTaskEntriesResponse(ListResponse[HumanTaskEntry]):
    """
    The response from listing human task entries
    """

    data: List[HumanTaskEntry] = Field(description="The list of human task entries")
