# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ToolSummarizeContentResponse", "Data"]


class Data(BaseModel):
    method: Literal["auto", "simple", "recursive", "multi_modal"]

    summary: str


class ToolSummarizeContentResponse(BaseModel):
    data: Data

    request_id: str

    seconds_taken: float
