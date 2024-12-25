# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from altmindpy import Altmind, AsyncAltmind
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExperimental:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_stream(self, client: Altmind) -> None:
        experimental = client.experimental.stream(
            content="content",
        )
        assert_matches_type(object, experimental, path=["response"])

    @parametrize
    def test_raw_response_stream(self, client: Altmind) -> None:
        response = client.experimental.with_raw_response.stream(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experimental = response.parse()
        assert_matches_type(object, experimental, path=["response"])

    @parametrize
    def test_streaming_response_stream(self, client: Altmind) -> None:
        with client.experimental.with_streaming_response.stream(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experimental = response.parse()
            assert_matches_type(object, experimental, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncExperimental:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_stream(self, async_client: AsyncAltmind) -> None:
        experimental = await async_client.experimental.stream(
            content="content",
        )
        assert_matches_type(object, experimental, path=["response"])

    @parametrize
    async def test_raw_response_stream(self, async_client: AsyncAltmind) -> None:
        response = await async_client.experimental.with_raw_response.stream(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experimental = await response.parse()
        assert_matches_type(object, experimental, path=["response"])

    @parametrize
    async def test_streaming_response_stream(self, async_client: AsyncAltmind) -> None:
        async with async_client.experimental.with_streaming_response.stream(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experimental = await response.parse()
            assert_matches_type(object, experimental, path=["response"])

        assert cast(Any, response.is_closed) is True
