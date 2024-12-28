# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import tool_search_web_params, tool_summarize_content_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.tool_search_web_response import ToolSearchWebResponse
from ..types.tool_summarize_content_response import ToolSummarizeContentResponse

__all__ = ["ToolsResource", "AsyncToolsResource"]


class ToolsResource(SyncAPIResource):
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

    def search_web(
        self,
        *,
        query: str,
        llm_answer: bool | NotGiven = NOT_GIVEN,
        top_n: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolSearchWebResponse:
        """
        Search the web for a given query

        Args:
          query: The query to search for

          llm_answer: Whether to return an LLM-generated answer instead of the search results

          top_n: The number of top results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/tools/search_web",
            body=maybe_transform(
                {
                    "query": query,
                    "llm_answer": llm_answer,
                    "top_n": top_n,
                },
                tool_search_web_params.ToolSearchWebParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ToolSearchWebResponse,
        )

    def summarize_content(
        self,
        *,
        content_id: str,
        method: Literal["auto", "simple", "recursive", "multi_modal"] | NotGiven = NOT_GIVEN,
        output_language: Literal["en", "pt", "es", "it", "de", "fr"] | NotGiven = NOT_GIVEN,
        source_type: Literal["youtube"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolSummarizeContentResponse:
        """
        Summarize The Contents Of The Given Source

        Args:
          content_id: The identifier of the content to summarize. Currently, only YouTube video URLs
              and IDs are supported

          method: The method to use for summarizing the content. Auto decides between 'simple' and
              'recursive' by length.

          output_language: The ISO 639-1 language code to use for the outputted summary. English (en) is
              recommended.

          source_type: The type of the content source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/tools/summarize_content",
            body=maybe_transform(
                {
                    "content_id": content_id,
                    "method": method,
                    "output_language": output_language,
                    "source_type": source_type,
                },
                tool_summarize_content_params.ToolSummarizeContentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ToolSummarizeContentResponse,
        )


class AsyncToolsResource(AsyncAPIResource):
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

    async def search_web(
        self,
        *,
        query: str,
        llm_answer: bool | NotGiven = NOT_GIVEN,
        top_n: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolSearchWebResponse:
        """
        Search the web for a given query

        Args:
          query: The query to search for

          llm_answer: Whether to return an LLM-generated answer instead of the search results

          top_n: The number of top results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/tools/search_web",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "llm_answer": llm_answer,
                    "top_n": top_n,
                },
                tool_search_web_params.ToolSearchWebParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ToolSearchWebResponse,
        )

    async def summarize_content(
        self,
        *,
        content_id: str,
        method: Literal["auto", "simple", "recursive", "multi_modal"] | NotGiven = NOT_GIVEN,
        output_language: Literal["en", "pt", "es", "it", "de", "fr"] | NotGiven = NOT_GIVEN,
        source_type: Literal["youtube"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolSummarizeContentResponse:
        """
        Summarize The Contents Of The Given Source

        Args:
          content_id: The identifier of the content to summarize. Currently, only YouTube video URLs
              and IDs are supported

          method: The method to use for summarizing the content. Auto decides between 'simple' and
              'recursive' by length.

          output_language: The ISO 639-1 language code to use for the outputted summary. English (en) is
              recommended.

          source_type: The type of the content source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/tools/summarize_content",
            body=await async_maybe_transform(
                {
                    "content_id": content_id,
                    "method": method,
                    "output_language": output_language,
                    "source_type": source_type,
                },
                tool_summarize_content_params.ToolSummarizeContentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ToolSummarizeContentResponse,
        )


class ToolsResourceWithRawResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

        self.search_web = to_raw_response_wrapper(
            tools.search_web,
        )
        self.summarize_content = to_raw_response_wrapper(
            tools.summarize_content,
        )


class AsyncToolsResourceWithRawResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

        self.search_web = async_to_raw_response_wrapper(
            tools.search_web,
        )
        self.summarize_content = async_to_raw_response_wrapper(
            tools.summarize_content,
        )


class ToolsResourceWithStreamingResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

        self.search_web = to_streamed_response_wrapper(
            tools.search_web,
        )
        self.summarize_content = to_streamed_response_wrapper(
            tools.summarize_content,
        )


class AsyncToolsResourceWithStreamingResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

        self.search_web = async_to_streamed_response_wrapper(
            tools.search_web,
        )
        self.summarize_content = async_to_streamed_response_wrapper(
            tools.summarize_content,
        )
