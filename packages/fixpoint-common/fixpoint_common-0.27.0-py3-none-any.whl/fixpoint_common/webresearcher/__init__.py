"""Web Researcher agent code"""

__all__ = [
    "AllResearchResultsJson",
    "AllResearchResultsPydantic",
    "convert_api_to_pydantic",
    "convert_json_to_api",
    "convert_json_to_pydantic",
    "CreateScrapeRequest",
    "ResearchResultWithSiteJson",
    "ResearchResultWithSitePydantic",
    "ScrapeResult",
]

from .types import (
    CreateScrapeRequest,
    ScrapeResult,
    ResearchResultWithSitePydantic,
    AllResearchResultsPydantic,
    ResearchResultWithSiteJson,
    AllResearchResultsJson,
)
from .converters import (
    convert_json_to_api,
    convert_json_to_pydantic,
    convert_api_to_pydantic,
)
