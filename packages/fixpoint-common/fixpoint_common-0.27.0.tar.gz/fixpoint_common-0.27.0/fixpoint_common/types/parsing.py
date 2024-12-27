"""
Types for parsing web pages and other data sources into an LLM-ready format.
"""

__all__ = [
    "CreateWebpageParseRequest",
    "WebpageParseResult",
    "CreateCrawlUrlParseRequest",
    "CrawlUrlParseResult",
    "Chunk",
    "OutputFormatType",
]


from typing import List, Optional, Literal

from pydantic import BaseModel, Field, field_validator


from .sources import BatchWebpageSource, WebpageSource, CrawlUrlSource
from ._shared import BaseRequest


OutputFormatType = Literal["markdown", "chunked_markdown"]
OutputMediaType = Literal["text/markdown"]

_OutputFormatsField = Field(
    default_factory=lambda: ["markdown"],
    # pylint: disable=line-too-long
    description="The output formats to use. Can specify multiple to get multiple formats in the response.",
)


def _validate_output_formats(v: List[OutputFormatType]) -> List[OutputFormatType]:
    assert len(v) > 0, "At least one output format must be specified"
    return v


class CreateWebpageParseRequest(BaseRequest):
    """Request to parse a single webpage.

    Parses a webpage and returns the text (non-chunked) of the page. The output
    format is markdown.
    """

    source: WebpageSource
    output_formats: List[OutputFormatType] = _OutputFormatsField

    _validate_output_formats = field_validator("output_formats")(
        _validate_output_formats
    )


class CreateBatchWebpageParseRequest(BaseRequest):
    """Request to parse a batch of webpages."""

    source: BatchWebpageSource
    output_formats: List[OutputFormatType] = _OutputFormatsField

    _validate_output_formats = field_validator("output_formats")(
        _validate_output_formats
    )


# Parse results are called `...ParseResult` instead of `...Parse` because if we
# have a plain `CreateParseRequest`, returning a `Parse` object is confusing
# about whether that is a verb or a noun.


class WebpageParseResult(BaseModel):
    """A parse result from a single webpage.

    Contains the text (non-chunked) of the page. The output format is markdown.
    """

    source: WebpageSource
    content: Optional[str] = Field(
        # pylint: disable=line-too-long
        description='The parsed text, ready for LLM. If you specify `output_formats` and don\'t include "markdown", this will be empty.'
    )
    content_media_type: Optional[OutputMediaType] = Field(
        description="The media type of the content."
    )
    chunks: Optional[List["Chunk"]] = Field(
        description="The parsed text, chunked into sections"
    )


class BatchWebpageParseResult(BaseModel):
    """A parse result from a batch of webpages."""

    results: List[WebpageParseResult]


class Chunk(BaseModel):
    """A chunk of text or media bytes."""

    media_type: OutputMediaType
    content: str


class CreateCrawlUrlParseRequest(BaseRequest):
    """Request to start a crawl parse.

    Crawls webpages starting at a URL. Returns the text (non-chunked) per page.
    The output format is markdown.
    """

    source: CrawlUrlSource
    output_formats: List[OutputFormatType] = _OutputFormatsField

    _validate_output_formats = field_validator("output_formats")(
        _validate_output_formats
    )


class CrawlUrlParseResult(BaseModel):
    """A parse result from crawling a URL.

    Contains the text (non-chunked) per page. The output format is markdown.
    """

    source: CrawlUrlSource
    page_contents: List[WebpageParseResult] = Field(
        description="The parsed contents of each page"
    )
