"""Types for patent extraction"""

__all__ = [
    "PatentExtraction",
    "PatentExtractionFilter",
    "PatentInfo",
    "CreatePatentExtractionRequest",
    "CreatePatentExtractionResponse",
]

import datetime
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, AfterValidator

from fixpoint_common.types.citations import Citation
from fixpoint_common.types.json_extraction import JsonSchemaExtraction
from fixpoint_common.types.research import ResearchRecord
from ._helpers import dt_to_utc


class PatentExtractionFilter(BaseModel):
    """
    Filters for patent extraction. All values are optional.
    When specified all filters are ANDed together.
    """

    keywords: Optional[List[str]] = Field(
        default=None, description="The keywords to filter by."
    )
    after_date: Optional[str] = Field(
        default=None, description="The date to filter by. Format: YYYYMMDD"
    )
    assignees: Optional[List[str]] = Field(
        default=None, description="The assignees to filter by."
    )


class CreatePatentExtractionRequest(BaseModel):
    """Request to create patent extraction."""

    run_id: Optional[str] = Field(description="The workflow run id.", default=None)
    questions: Optional[List[str]] = Field(
        description="The questions to answer.", default_factory=list
    )
    filters: Optional[PatentExtractionFilter] = Field(
        default=None, description="The filters to apply to the extraction."
    )


class PatentInfo(BaseModel):
    """Information about a patent."""

    patent_number: str = Field(description="The patent number.")
    inventors: str = Field(description="The inventors.")
    assignees: str = Field(description="The assignees.")
    filing_date: Annotated[datetime.datetime, AfterValidator(dt_to_utc)] = Field(
        description="The filing date.",
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    publication_date: Annotated[datetime.datetime, AfterValidator(dt_to_utc)] = Field(
        description="The publication date.",
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    title: str = Field(description="The title.")
    summary: str = Field(description="The summary.")


class PatentExtraction(BaseModel):
    """Extraction result from a patent search extraction."""

    patent_info: PatentInfo = Field(description="The patent information.")
    result_record: Optional[ResearchRecord] = Field(
        description="Data extracted based on your extraction questions",
        default=None,
    )
    citations: List[Citation] = Field(
        description="The citations for the extraction result."
    )
    sub_json_extractions: List[JsonSchemaExtraction] = Field(
        description="The sub-extractions that resulted in this extraction."
    )


class CreatePatentExtractionResponse(BaseModel):
    """Response to create patent extraction."""

    patent_extractions: List[PatentExtraction] = Field(
        description="The patent extractions."
    )
