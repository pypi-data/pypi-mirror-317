"""
Conversions between JSON, API request/response, and Pydantic models for the
WebResearcher agent.
"""

__all__ = ["convert_json_to_api", "convert_json_to_pydantic", "convert_api_to_pydantic"]

from typing import Type, TypeVar

from pydantic import BaseModel

from .types import (
    AllResearchResultsJson,
    AllResearchResultsPydantic,
    ResearchResultWithSitePydantic,
    ScrapeResult as ScrapeResultApi,
    ScrapeSiteResult as ScrapeSiteResultApi,
)


BM = TypeVar("BM", bound=BaseModel)


def convert_json_to_api(
    workflow_id: str, workflow_run_id: str, json_obj: AllResearchResultsJson
) -> ScrapeResultApi:
    """Convert JSON research results to a research results API response."""
    return ScrapeResultApi(
        workflow_id=workflow_id,
        workflow_run_id=workflow_run_id,
        results=[
            ScrapeSiteResultApi(
                site=result.site,
                result=result.result,
            )
            for result in json_obj.results
        ],
    )


def convert_json_to_pydantic(
    model_schema: Type[BM], json_obj: AllResearchResultsJson
) -> AllResearchResultsPydantic[BM]:
    """Convert JSON research results to a Pydantic research results."""
    return AllResearchResultsPydantic(
        results=[
            ResearchResultWithSitePydantic(
                site=result.site,
                result=model_schema.model_validate(result.result),
            )
            for result in json_obj.results
        ],
    )


def convert_api_to_pydantic(
    model_schema: Type[BM], api_obj: ScrapeResultApi
) -> AllResearchResultsPydantic[BM]:
    """Convert research results API response to a Pydantic research results."""
    return AllResearchResultsPydantic(
        results=[
            ResearchResultWithSitePydantic(
                site=result.site,
                result=model_schema.model_validate(result.result),
            )
            for result in api_obj.results
        ],
    )
