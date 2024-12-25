# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["SearchResponseBundle", "Llm", "Result"]


class Llm(BaseModel):
    answer: str

    answerable_probability: float


class Result(BaseModel):
    content: str

    score: float

    source_url: str


class SearchResponseBundle(BaseModel):
    llm: Optional[Llm] = None

    query: Optional[str] = None

    results: Optional[List[Result]] = None

    total_results: Optional[int] = None
    """Total number of results found"""
