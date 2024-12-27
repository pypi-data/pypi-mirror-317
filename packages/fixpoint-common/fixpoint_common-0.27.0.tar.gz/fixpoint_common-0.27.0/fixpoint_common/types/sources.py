"""
Types for sources of data to parse into LLM-ready text or to extract data from.
"""

__all__ = ["Source", "TextSource", "WebpageSource", "CrawlUrlSource", "BatchTextSource"]

from typing import Literal, List, Optional, Union

from pydantic import BaseModel, Field


class TextSource(BaseModel):
    """Extract or parse data from a text file."""

    kind: Literal["text"] = Field(
        description="The type of extraction or parse source.", default="text"
    )
    text_id: str = Field(description="The ID for the text file.")
    content: str = Field(description="The content of the text file.")


class BatchTextSource(BaseModel):
    """Extract or parse data from a batch of text files."""

    kind: Literal["batch_text"] = Field(
        description="The type of extraction or parse source.", default="batch_text"
    )
    sources: List[TextSource] = Field(description="The sources to extract data from.")


class WebpageSource(BaseModel):
    """Extract or parse data from a single web page"""

    kind: Literal["web_page"] = Field(
        description="The type of extraction or parse source.", default="web_page"
    )
    url: str = Field(description="The URL to extract data from.")


class BatchWebpageSource(BaseModel):
    """Extract or parse data from a batch of web pages"""

    kind: Literal["batch_web_page"] = Field(
        description="The type of extraction or parse source.", default="batch_web_page"
    )
    urls: List[str] = Field(description="The URLs to extract data from.")


class CrawlUrlSource(BaseModel):
    """Extract or parse data from multiple pages by crawling a starting URL"""

    kind: Literal["crawl_url"] = Field(
        description="The type of extraction or parse source", default="crawl_url"
    )
    # We use "crawl_url" instead of "url" so that it is possible to distinguish
    # a `CrawlUrlSource` from a `WebpageSource`, even if the caller does not
    # specify `kind`.
    crawl_url: str = Field(description="The URL to start crawling from.")
    depth: Optional[int] = Field(description="The depth of the crawl", default=2)
    page_limit: Optional[int] = Field(
        description="The maximum number of pages to crawl", default=20
    )


Source = Union[TextSource, WebpageSource, CrawlUrlSource, BatchTextSource]
