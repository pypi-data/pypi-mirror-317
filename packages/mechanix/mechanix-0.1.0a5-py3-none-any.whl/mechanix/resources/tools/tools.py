# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .search import (
    SearchResource,
    AsyncSearchResource,
    SearchResourceWithRawResponse,
    AsyncSearchResourceWithRawResponse,
    SearchResourceWithStreamingResponse,
    AsyncSearchResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .summarize import (
    SummarizeResource,
    AsyncSummarizeResource,
    SummarizeResourceWithRawResponse,
    AsyncSummarizeResourceWithRawResponse,
    SummarizeResourceWithStreamingResponse,
    AsyncSummarizeResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["ToolsResource", "AsyncToolsResource"]


class ToolsResource(SyncAPIResource):
    @cached_property
    def search(self) -> SearchResource:
        return SearchResource(self._client)

    @cached_property
    def summarize(self) -> SummarizeResource:
        return SummarizeResource(self._client)

    @cached_property
    def with_raw_response(self) -> ToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#accessing-raw-response-data-eg-headers
        """
        return ToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#with_streaming_response
        """
        return ToolsResourceWithStreamingResponse(self)


class AsyncToolsResource(AsyncAPIResource):
    @cached_property
    def search(self) -> AsyncSearchResource:
        return AsyncSearchResource(self._client)

    @cached_property
    def summarize(self) -> AsyncSummarizeResource:
        return AsyncSummarizeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#with_streaming_response
        """
        return AsyncToolsResourceWithStreamingResponse(self)


class ToolsResourceWithRawResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

    @cached_property
    def search(self) -> SearchResourceWithRawResponse:
        return SearchResourceWithRawResponse(self._tools.search)

    @cached_property
    def summarize(self) -> SummarizeResourceWithRawResponse:
        return SummarizeResourceWithRawResponse(self._tools.summarize)


class AsyncToolsResourceWithRawResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

    @cached_property
    def search(self) -> AsyncSearchResourceWithRawResponse:
        return AsyncSearchResourceWithRawResponse(self._tools.search)

    @cached_property
    def summarize(self) -> AsyncSummarizeResourceWithRawResponse:
        return AsyncSummarizeResourceWithRawResponse(self._tools.summarize)


class ToolsResourceWithStreamingResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

    @cached_property
    def search(self) -> SearchResourceWithStreamingResponse:
        return SearchResourceWithStreamingResponse(self._tools.search)

    @cached_property
    def summarize(self) -> SummarizeResourceWithStreamingResponse:
        return SummarizeResourceWithStreamingResponse(self._tools.summarize)


class AsyncToolsResourceWithStreamingResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

    @cached_property
    def search(self) -> AsyncSearchResourceWithStreamingResponse:
        return AsyncSearchResourceWithStreamingResponse(self._tools.search)

    @cached_property
    def summarize(self) -> AsyncSummarizeResourceWithStreamingResponse:
        return AsyncSummarizeResourceWithStreamingResponse(self._tools.summarize)
