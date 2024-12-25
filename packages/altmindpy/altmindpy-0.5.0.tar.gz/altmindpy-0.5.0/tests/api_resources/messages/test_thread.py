# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from altmindpy import Altmind, AsyncAltmind
from tests.utils import assert_matches_type
from altmindpy.types import MessagesResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThread:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Altmind) -> None:
        thread = client.messages.thread.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessagesResponse, thread, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Altmind) -> None:
        thread = client.messages.thread.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=0,
            offset=0,
        )
        assert_matches_type(MessagesResponse, thread, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Altmind) -> None:
        response = client.messages.thread.with_raw_response.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(MessagesResponse, thread, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Altmind) -> None:
        with client.messages.thread.with_streaming_response.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(MessagesResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.messages.thread.with_raw_response.list(
                thread_id="",
            )


class TestAsyncThread:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncAltmind) -> None:
        thread = await async_client.messages.thread.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessagesResponse, thread, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAltmind) -> None:
        thread = await async_client.messages.thread.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=0,
            offset=0,
        )
        assert_matches_type(MessagesResponse, thread, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAltmind) -> None:
        response = await async_client.messages.thread.with_raw_response.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(MessagesResponse, thread, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAltmind) -> None:
        async with async_client.messages.thread.with_streaming_response.list(
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(MessagesResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.messages.thread.with_raw_response.list(
                thread_id="",
            )
