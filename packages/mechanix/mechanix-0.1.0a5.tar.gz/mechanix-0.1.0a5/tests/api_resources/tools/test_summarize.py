# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mechanix import Mechanix, AsyncMechanix
from tests.utils import assert_matches_type
from mechanix.types.tools import SummaryItem

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSummarize:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_youtube(self, client: Mechanix) -> None:
        summarize = client.tools.summarize.youtube(
            video="5qSrmeiWsuc",
        )
        assert_matches_type(SummaryItem, summarize, path=["response"])

    @parametrize
    def test_method_youtube_with_all_params(self, client: Mechanix) -> None:
        summarize = client.tools.summarize.youtube(
            video="5qSrmeiWsuc",
            method="auto",
            output_language="en",
        )
        assert_matches_type(SummaryItem, summarize, path=["response"])

    @parametrize
    def test_raw_response_youtube(self, client: Mechanix) -> None:
        response = client.tools.summarize.with_raw_response.youtube(
            video="5qSrmeiWsuc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        summarize = response.parse()
        assert_matches_type(SummaryItem, summarize, path=["response"])

    @parametrize
    def test_streaming_response_youtube(self, client: Mechanix) -> None:
        with client.tools.summarize.with_streaming_response.youtube(
            video="5qSrmeiWsuc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            summarize = response.parse()
            assert_matches_type(SummaryItem, summarize, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSummarize:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_youtube(self, async_client: AsyncMechanix) -> None:
        summarize = await async_client.tools.summarize.youtube(
            video="5qSrmeiWsuc",
        )
        assert_matches_type(SummaryItem, summarize, path=["response"])

    @parametrize
    async def test_method_youtube_with_all_params(self, async_client: AsyncMechanix) -> None:
        summarize = await async_client.tools.summarize.youtube(
            video="5qSrmeiWsuc",
            method="auto",
            output_language="en",
        )
        assert_matches_type(SummaryItem, summarize, path=["response"])

    @parametrize
    async def test_raw_response_youtube(self, async_client: AsyncMechanix) -> None:
        response = await async_client.tools.summarize.with_raw_response.youtube(
            video="5qSrmeiWsuc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        summarize = await response.parse()
        assert_matches_type(SummaryItem, summarize, path=["response"])

    @parametrize
    async def test_streaming_response_youtube(self, async_client: AsyncMechanix) -> None:
        async with async_client.tools.summarize.with_streaming_response.youtube(
            video="5qSrmeiWsuc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            summarize = await response.parse()
            assert_matches_type(SummaryItem, summarize, path=["response"])

        assert cast(Any, response.is_closed) is True
