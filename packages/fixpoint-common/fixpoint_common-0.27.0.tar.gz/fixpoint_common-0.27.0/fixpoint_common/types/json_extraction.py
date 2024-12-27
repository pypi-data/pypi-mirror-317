"""Types for JSON schema extractions."""

__all__ = [
    "CreateJsonSchemaExtractionRequest",
    "JsonSchemaExtraction",
]

from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from openai.types.completion_usage import CompletionUsage

from fixpoint_common.types.sources import TextSource, WebpageSource
from fixpoint_common.types.workflow import WorkflowRunId
from fixpoint_common.completions import ChatCompletionMessageParam
from .citations import Citation


class JsonSchemaExtraction(BaseModel):
    """Extraction result from a JSON schema extraction."""

    result: Dict[str, Any] = Field(description="The extraction result.")
    citations: List[Citation] = Field(
        description="The citations for the extraction result."
    )
    ai_model: str = Field(description="The model used to generate the extraction.")
    completion_usage: Optional[CompletionUsage] = Field(
        description="The completion usage for the extraction.",
        default=None,
    )


class CreateJsonSchemaExtractionRequest(BaseModel):
    """Request to create a JSON schema extraction."""

    run_id: Optional[WorkflowRunId] = None
    source: Union[TextSource, WebpageSource] = Field(
        description="The source of the data to extract."
    )

    # We cannot directly name this "schema" because that's a reserved word in
    # Pydantic, but we can set an "alias" so that users can pass in "schema" to
    # in the API.
    schema_: Dict[str, Any] = Field(
        description="The JSON schema for the extraction results",
        min_length=1,
        alias="schema",
    )

    extra_instructions: Optional[List[ChatCompletionMessageParam]] = Field(
        description="Additional instruction messages to prepend to the prompt",
        default=None,
    )
