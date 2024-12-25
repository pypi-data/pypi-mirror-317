# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mechanix import Mechanix, AsyncMechanix
from tests.utils import assert_matches_type
from mechanix.types import UserModel

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_view(self, client: Mechanix) -> None:
        user = client.users.view(
            email="dev@stainlessapi.com",
            password="password",
        )
        assert_matches_type(UserModel, user, path=["response"])

    @parametrize
    def test_raw_response_view(self, client: Mechanix) -> None:
        response = client.users.with_raw_response.view(
            email="dev@stainlessapi.com",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserModel, user, path=["response"])

    @parametrize
    def test_streaming_response_view(self, client: Mechanix) -> None:
        with client.users.with_streaming_response.view(
            email="dev@stainlessapi.com",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserModel, user, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_view(self, async_client: AsyncMechanix) -> None:
        user = await async_client.users.view(
            email="dev@stainlessapi.com",
            password="password",
        )
        assert_matches_type(UserModel, user, path=["response"])

    @parametrize
    async def test_raw_response_view(self, async_client: AsyncMechanix) -> None:
        response = await async_client.users.with_raw_response.view(
            email="dev@stainlessapi.com",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserModel, user, path=["response"])

    @parametrize
    async def test_streaming_response_view(self, async_client: AsyncMechanix) -> None:
        async with async_client.users.with_streaming_response.view(
            email="dev@stainlessapi.com",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserModel, user, path=["response"])

        assert cast(Any, response.is_closed) is True
