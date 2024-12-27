# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPromptTemplates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Evrim) -> None:
        prompt_template = client.prompt_templates.create(
            prompt="prompt",
        )
        assert prompt_template is None

    @parametrize
    def test_raw_response_create(self, client: Evrim) -> None:
        response = client.prompt_templates.with_raw_response.create(
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_template = response.parse()
        assert prompt_template is None

    @parametrize
    def test_streaming_response_create(self, client: Evrim) -> None:
        with client.prompt_templates.with_streaming_response.create(
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_template = response.parse()
            assert prompt_template is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_save(self, client: Evrim) -> None:
        prompt_template = client.prompt_templates.save(
            template={},
        )
        assert prompt_template is None

    @parametrize
    def test_raw_response_save(self, client: Evrim) -> None:
        response = client.prompt_templates.with_raw_response.save(
            template={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_template = response.parse()
        assert prompt_template is None

    @parametrize
    def test_streaming_response_save(self, client: Evrim) -> None:
        with client.prompt_templates.with_streaming_response.save(
            template={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_template = response.parse()
            assert prompt_template is None

        assert cast(Any, response.is_closed) is True


class TestAsyncPromptTemplates:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEvrim) -> None:
        prompt_template = await async_client.prompt_templates.create(
            prompt="prompt",
        )
        assert prompt_template is None

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEvrim) -> None:
        response = await async_client.prompt_templates.with_raw_response.create(
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_template = await response.parse()
        assert prompt_template is None

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEvrim) -> None:
        async with async_client.prompt_templates.with_streaming_response.create(
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_template = await response.parse()
            assert prompt_template is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_save(self, async_client: AsyncEvrim) -> None:
        prompt_template = await async_client.prompt_templates.save(
            template={},
        )
        assert prompt_template is None

    @parametrize
    async def test_raw_response_save(self, async_client: AsyncEvrim) -> None:
        response = await async_client.prompt_templates.with_raw_response.save(
            template={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_template = await response.parse()
        assert prompt_template is None

    @parametrize
    async def test_streaming_response_save(self, async_client: AsyncEvrim) -> None:
        async with async_client.prompt_templates.with_streaming_response.save(
            template={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_template = await response.parse()
            assert prompt_template is None

        assert cast(Any, response.is_closed) is True
