"""RESTful API types and helpers"""

__all__ = [
    "CreateScrapeRequest",
    "ScrapeResult",
    "ResearchResultWithSitePydantic",
    "AllResearchResultsPydantic",
    "ResearchResultWithSiteJson",
    "AllResearchResultsJson",
]

from typing import Any, Dict, Generic, List, Optional

from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, Field, HttpUrl, field_serializer

from fixpoint_common.types.basic import BM
from fixpoint_common.completions import ChatCompletionMessageParam


class CreateScrapeRequest(BaseModel):
    """A request to create a scrape workflow.

    A request to create a scrape workflow, for use with the Fixpoint RESTful
    API.
    """

    workflow_id: str = Field(
        description="The ID for the scrape workflow",
        min_length=1,
    )
    run_id: Optional[str] = Field(
        description="If retrying a workflow run, the run ID to respawn",
        default=None,
    )

    site: HttpUrl = Field(description="The site to scrape")

    @field_serializer("site")
    def _serialize_site(self, site: HttpUrl) -> str:
        return str(site)

    # For now, multi-site support is not allowed until we have better support
    # for long-running web research workflows.

    # sites: List[str] = Field(
    #     description="The list of sites to scrape",
    #     min_length=1,
    # )

    research_schema: Dict[str, Any] = Field(
        description="The JSON schema for the research extraction results",
        min_length=1,
    )
    extra_instructions: Optional[List[ChatCompletionMessageParam]] = Field(
        description="Additional instruction messages to prepend to the prompt",
        default=None,
    )


class ScrapeSiteResult(BaseModel):
    """Your research results, tagged with the site they came from."""

    site: str
    result: Dict[str, Any]


class ScrapeResult(BaseModel):
    """The research results per site, across all sites."""

    workflow_id: str
    workflow_run_id: str
    results: List[ScrapeSiteResult]


class ResearchResultWithSitePydantic(BaseModel, Generic[BM]):
    """Your research results, tagged with the site they came from."""

    site: str
    result: BM


class AllResearchResultsPydantic(BaseModel, Generic[BM]):
    """The research results per site, across all sites."""

    results: List[ResearchResultWithSitePydantic[BM]]


class ResearchResultWithSiteJson(BaseModel):
    """Your research results, tagged with the site they came from."""

    site: str
    result: Dict[str, Any]
    completion_usage: Optional[CompletionUsage] = Field(
        description="The completion usage for the extraction.",
        default=None,
    )


class AllResearchResultsJson(BaseModel):
    """The research results per site, across all sites."""

    results: List[ResearchResultWithSiteJson]
