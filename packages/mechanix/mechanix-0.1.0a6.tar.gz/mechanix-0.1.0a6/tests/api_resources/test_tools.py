# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mechanix import Mechanix, AsyncMechanix
from tests.utils import assert_matches_type
from mechanix.types import (
    ToolSearchWebResponse,
    ToolSummarizeContentResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTools:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_search_web(self, client: Mechanix) -> None:
        tool = client.tools.search_web(
            query="Common organelles within a human eukaryote",
        )
        assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

    @parametrize
    def test_method_search_web_with_all_params(self, client: Mechanix) -> None:
        tool = client.tools.search_web(
            query="Common organelles within a human eukaryote",
            llm_answer=True,
            top_n=1,
        )
        assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

    @parametrize
    def test_raw_response_search_web(self, client: Mechanix) -> None:
        response = client.tools.with_raw_response.search_web(
            query="Common organelles within a human eukaryote",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

    @parametrize
    def test_streaming_response_search_web(self, client: Mechanix) -> None:
        with client.tools.with_streaming_response.search_web(
            query="Common organelles within a human eukaryote",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_summarize_content(self, client: Mechanix) -> None:
        tool = client.tools.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
        )
        assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

    @parametrize
    def test_method_summarize_content_with_all_params(self, client: Mechanix) -> None:
        tool = client.tools.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
            method="auto",
            output_language="en",
            source_type="youtube",
        )
        assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

    @parametrize
    def test_raw_response_summarize_content(self, client: Mechanix) -> None:
        response = client.tools.with_raw_response.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

    @parametrize
    def test_streaming_response_summarize_content(self, client: Mechanix) -> None:
        with client.tools.with_streaming_response.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTools:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_search_web(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.search_web(
            query="Common organelles within a human eukaryote",
        )
        assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

    @parametrize
    async def test_method_search_web_with_all_params(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.search_web(
            query="Common organelles within a human eukaryote",
            llm_answer=True,
            top_n=1,
        )
        assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

    @parametrize
    async def test_raw_response_search_web(self, async_client: AsyncMechanix) -> None:
        response = await async_client.tools.with_raw_response.search_web(
            query="Common organelles within a human eukaryote",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

    @parametrize
    async def test_streaming_response_search_web(self, async_client: AsyncMechanix) -> None:
        async with async_client.tools.with_streaming_response.search_web(
            query="Common organelles within a human eukaryote",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(ToolSearchWebResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_summarize_content(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
        )
        assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

    @parametrize
    async def test_method_summarize_content_with_all_params(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
            method="auto",
            output_language="en",
            source_type="youtube",
        )
        assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

    @parametrize
    async def test_raw_response_summarize_content(self, async_client: AsyncMechanix) -> None:
        response = await async_client.tools.with_raw_response.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

    @parametrize
    async def test_streaming_response_summarize_content(self, async_client: AsyncMechanix) -> None:
        async with async_client.tools.with_streaming_response.summarize_content(
            content_id="https://www.youtube.com/watch?v=5qSrmeiWsuc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(ToolSummarizeContentResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True
