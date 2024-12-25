# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SummaryItem"]


class SummaryItem(BaseModel):
    method: Literal["auto", "simple", "recursive", "multi_modal"]

    summary: str
