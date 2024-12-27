"""Types for extraction requests and responses."""

__all__ = [
    "CreateRecordExtractionRequest",
    "RecordExtraction",
    "CreateBatchExtractionJobRequest",
    "BatchExtractionJob",
    "BatchExtractionJobStatus",
]

from typing import Optional, Union, List
from pydantic import BaseModel, Field

from fixpoint_common.completions import ChatCompletionMessageParam
from fixpoint_common.types.json_extraction import (
    JsonSchemaExtraction,
)
from fixpoint_common.types.metadata import Metadata
from .citations import Citation
from .research import ResearchRecord
from .sources import TextSource, WebpageSource, CrawlUrlSource, BatchTextSource
from .workflow import WorkflowRunId


class CreateRecordExtractionRequest(BaseModel):
    """Request to create Record Q&A extraction."""

    document_id: Optional[str] = None
    document_name: Optional[str] = None
    run_id: Optional[WorkflowRunId] = None

    source: Union[
        CrawlUrlSource,
        WebpageSource,
        TextSource,
        BatchTextSource,
    ] = Field(description="The source of the data to extract.")

    extra_instructions: Optional[List[ChatCompletionMessageParam]] = Field(
        description="Additional prompt instructions",
        default=None,
    )

    questions: List[str] = Field(description="The questions to answer.")

    metadata: Optional[Metadata] = Field(
        default=None, description="Metadata for document"
    )


class RecordExtraction(BaseModel):
    """Extraction result from a question and answer record extraction."""

    result_record: ResearchRecord = Field(
        description="The research record containing the extracted data."
    )
    citations: List[Citation] = Field(
        description="The citations for the extraction result."
    )
    sub_json_extractions: List[JsonSchemaExtraction] = Field(
        description="The sub-extractions that resulted in this extraction."
    )


class CreateBatchExtractionJobRequest(BaseModel):
    """A request to create a batch extraction job."""

    job_id: Optional[str] = None
    document_id: Optional[str] = None
    requests: List[CreateRecordExtractionRequest]


class BatchExtractionJob(BaseModel):
    """A response to a create batch extract job request."""

    job_id: str


class BatchExtractionJobStatus(BaseModel):
    """A response to a get batch extraction job status request."""

    job_id: str
    completed: int
    failed: int
    pending: int
