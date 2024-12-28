# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ToolSummarizeContentParams"]


class ToolSummarizeContentParams(TypedDict, total=False):
    content_id: Required[str]
    """The identifier of the content to summarize.

    Currently, only YouTube video URLs and IDs are supported
    """

    method: Literal["auto", "simple", "recursive", "multi_modal"]
    """The method to use for summarizing the content.

    Auto decides between 'simple' and 'recursive' by length.
    """

    output_language: Literal["en", "pt", "es", "it", "de", "fr"]
    """The ISO 639-1 language code to use for the outputted summary.

    English (en) is recommended.
    """

    source_type: Literal["youtube"]
    """The type of the content source."""
