# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.tools import summarize_youtube_params
from ..._base_client import make_request_options
from ...types.tools.summary_item import SummaryItem

__all__ = ["SummarizeResource", "AsyncSummarizeResource"]


class SummarizeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SummarizeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#accessing-raw-response-data-eg-headers
        """
        return SummarizeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SummarizeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#with_streaming_response
        """
        return SummarizeResourceWithStreamingResponse(self)

    def youtube(
        self,
        *,
        video: str,
        method: Literal["auto", "simple", "recursive", "multi_modal"] | NotGiven = NOT_GIVEN,
        output_language: Literal["en", "pt", "es", "it", "de", "fr"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SummaryItem:
        """
        Summarize The Contents Of The Given Source

        Args:
          video: The ID of the YouTube video to summarize. Full URLs and other forms may be
              accepted, but may not be correctly parsed.

          method: The method to use for summarizing the content. Auto decides between 'simple' and
              'recursive' by length.

          output_language: The ISO 639-1 langauge code to use for the outputted summary. English (en) is
              recommended.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/tools/summarize/youtube",
            body=maybe_transform(
                {
                    "video": video,
                    "method": method,
                    "output_language": output_language,
                },
                summarize_youtube_params.SummarizeYoutubeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SummaryItem,
        )


class AsyncSummarizeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSummarizeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSummarizeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSummarizeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#with_streaming_response
        """
        return AsyncSummarizeResourceWithStreamingResponse(self)

    async def youtube(
        self,
        *,
        video: str,
        method: Literal["auto", "simple", "recursive", "multi_modal"] | NotGiven = NOT_GIVEN,
        output_language: Literal["en", "pt", "es", "it", "de", "fr"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SummaryItem:
        """
        Summarize The Contents Of The Given Source

        Args:
          video: The ID of the YouTube video to summarize. Full URLs and other forms may be
              accepted, but may not be correctly parsed.

          method: The method to use for summarizing the content. Auto decides between 'simple' and
              'recursive' by length.

          output_language: The ISO 639-1 langauge code to use for the outputted summary. English (en) is
              recommended.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/tools/summarize/youtube",
            body=await async_maybe_transform(
                {
                    "video": video,
                    "method": method,
                    "output_language": output_language,
                },
                summarize_youtube_params.SummarizeYoutubeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SummaryItem,
        )


class SummarizeResourceWithRawResponse:
    def __init__(self, summarize: SummarizeResource) -> None:
        self._summarize = summarize

        self.youtube = to_raw_response_wrapper(
            summarize.youtube,
        )


class AsyncSummarizeResourceWithRawResponse:
    def __init__(self, summarize: AsyncSummarizeResource) -> None:
        self._summarize = summarize

        self.youtube = async_to_raw_response_wrapper(
            summarize.youtube,
        )


class SummarizeResourceWithStreamingResponse:
    def __init__(self, summarize: SummarizeResource) -> None:
        self._summarize = summarize

        self.youtube = to_streamed_response_wrapper(
            summarize.youtube,
        )


class AsyncSummarizeResourceWithStreamingResponse:
    def __init__(self, summarize: AsyncSummarizeResource) -> None:
        self._summarize = summarize

        self.youtube = async_to_streamed_response_wrapper(
            summarize.youtube,
        )
