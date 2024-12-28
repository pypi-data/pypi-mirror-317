# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ToolSearchWebParams"]


class ToolSearchWebParams(TypedDict, total=False):
    query: Required[str]
    """The query to search for"""

    llm_answer: bool
    """Whether to return an LLM-generated answer instead of the search results"""

    top_n: int
    """The number of top results to return"""
