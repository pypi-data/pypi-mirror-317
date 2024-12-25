# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SummarizeYoutubeParams"]


class SummarizeYoutubeParams(TypedDict, total=False):
    video: Required[str]
    """The ID of the YouTube video to summarize.

    Full URLs and other forms may be accepted, but may not be correctly parsed.
    """

    method: Literal["auto", "simple", "recursive", "multi_modal"]
    """The method to use for summarizing the content.

    Auto decides between 'simple' and 'recursive' by length.
    """

    output_language: Literal["en", "pt", "es", "it", "de", "fr"]
    """The ISO 639-1 langauge code to use for the outputted summary.

    English (en) is recommended.
    """
