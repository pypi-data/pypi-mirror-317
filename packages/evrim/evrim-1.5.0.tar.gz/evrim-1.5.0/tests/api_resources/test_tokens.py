# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from evrim.types import (
    TokenVerify,
    TokenRefresh,
    TokenObtainPair,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTokens:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Evrim) -> None:
        token = client.tokens.create(
            password="password",
            username="username",
        )
        assert_matches_type(TokenObtainPair, token, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Evrim) -> None:
        response = client.tokens.with_raw_response.create(
            password="password",
            username="username",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = response.parse()
        assert_matches_type(TokenObtainPair, token, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Evrim) -> None:
        with client.tokens.with_streaming_response.create(
            password="password",
            username="username",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = response.parse()
            assert_matches_type(TokenObtainPair, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_refresh(self, client: Evrim) -> None:
        token = client.tokens.refresh(
            refresh="refresh",
        )
        assert_matches_type(TokenRefresh, token, path=["response"])

    @parametrize
    def test_raw_response_refresh(self, client: Evrim) -> None:
        response = client.tokens.with_raw_response.refresh(
            refresh="refresh",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = response.parse()
        assert_matches_type(TokenRefresh, token, path=["response"])

    @parametrize
    def test_streaming_response_refresh(self, client: Evrim) -> None:
        with client.tokens.with_streaming_response.refresh(
            refresh="refresh",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = response.parse()
            assert_matches_type(TokenRefresh, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_verify(self, client: Evrim) -> None:
        token = client.tokens.verify(
            token="token",
        )
        assert_matches_type(TokenVerify, token, path=["response"])

    @parametrize
    def test_raw_response_verify(self, client: Evrim) -> None:
        response = client.tokens.with_raw_response.verify(
            token="token",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = response.parse()
        assert_matches_type(TokenVerify, token, path=["response"])

    @parametrize
    def test_streaming_response_verify(self, client: Evrim) -> None:
        with client.tokens.with_streaming_response.verify(
            token="token",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = response.parse()
            assert_matches_type(TokenVerify, token, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTokens:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEvrim) -> None:
        token = await async_client.tokens.create(
            password="password",
            username="username",
        )
        assert_matches_type(TokenObtainPair, token, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEvrim) -> None:
        response = await async_client.tokens.with_raw_response.create(
            password="password",
            username="username",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = await response.parse()
        assert_matches_type(TokenObtainPair, token, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEvrim) -> None:
        async with async_client.tokens.with_streaming_response.create(
            password="password",
            username="username",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = await response.parse()
            assert_matches_type(TokenObtainPair, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_refresh(self, async_client: AsyncEvrim) -> None:
        token = await async_client.tokens.refresh(
            refresh="refresh",
        )
        assert_matches_type(TokenRefresh, token, path=["response"])

    @parametrize
    async def test_raw_response_refresh(self, async_client: AsyncEvrim) -> None:
        response = await async_client.tokens.with_raw_response.refresh(
            refresh="refresh",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = await response.parse()
        assert_matches_type(TokenRefresh, token, path=["response"])

    @parametrize
    async def test_streaming_response_refresh(self, async_client: AsyncEvrim) -> None:
        async with async_client.tokens.with_streaming_response.refresh(
            refresh="refresh",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = await response.parse()
            assert_matches_type(TokenRefresh, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_verify(self, async_client: AsyncEvrim) -> None:
        token = await async_client.tokens.verify(
            token="token",
        )
        assert_matches_type(TokenVerify, token, path=["response"])

    @parametrize
    async def test_raw_response_verify(self, async_client: AsyncEvrim) -> None:
        response = await async_client.tokens.with_raw_response.verify(
            token="token",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = await response.parse()
        assert_matches_type(TokenVerify, token, path=["response"])

    @parametrize
    async def test_streaming_response_verify(self, async_client: AsyncEvrim) -> None:
        async with async_client.tokens.with_streaming_response.verify(
            token="token",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = await response.parse()
            assert_matches_type(TokenVerify, token, path=["response"])

        assert cast(Any, response.is_closed) is True
