"""Types for the Fixpoint package"""

__all__ = [
    "ListResponse",
]

from typing import (
    Generic,
    List,
    Literal,
    Optional,
    TypeVar,
)

from pydantic import BaseModel, Field


BM = TypeVar("BM", bound=BaseModel)


# TODO(jakub): Add total number of results and pages to the API below
class ListResponse(BaseModel, Generic[BM]):
    """An API list response"""

    data: List[BM] = Field(description="The list of items")
    next_page_token: Optional[str] = Field(
        default=None,
        description="Token to get the next page of results. If no more pages, it is None",
    )
    kind: Literal["list"] = "list"
