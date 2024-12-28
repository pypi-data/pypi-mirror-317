# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ToolSearchWebResponse", "Data", "DataLlm", "DataResult"]


class DataLlm(BaseModel):
    answer: str

    answerable_probability: float


class DataResult(BaseModel):
    content: str

    score: float

    source_url: str


class Data(BaseModel):
    llm: Optional[DataLlm] = None

    query: Optional[str] = None

    results: Optional[List[DataResult]] = None

    total_results: Optional[int] = None
    """Total number of results found"""


class ToolSearchWebResponse(BaseModel):
    data: Data
    """Container for search results with optional metadata"""

    request_id: str

    seconds_taken: float
