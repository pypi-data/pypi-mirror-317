"""Citations for extractions and research records"""

__all__ = ["WebPageCitation", "TextCitation", "Citation"]

from typing import Literal, Union

from pydantic import BaseModel, Field


class WebPageCitation(BaseModel):
    """A citation from a web page"""

    kind: Literal["web_page_citation"]
    url: str = Field(description="The URL for the web page.")


class TextCitation(BaseModel):
    """A citation from a plain text source"""

    kind: Literal["text_citation"]
    text_id: str = Field(description="The ID for the text file.")
    text_start: int = Field(description="The start index of the text citation.")
    text_end: int = Field(description="The end index of the text citation.")


Citation = Union[WebPageCitation, TextCitation]
