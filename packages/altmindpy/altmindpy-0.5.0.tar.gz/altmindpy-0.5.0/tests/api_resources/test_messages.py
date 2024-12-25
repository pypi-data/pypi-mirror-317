# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from altmindpy import Altmind, AsyncAltmind
from tests.utils import assert_matches_type
from altmindpy.types import (
    MessageDelete,
    MessageResponse,
    MessagesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMessages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Altmind) -> None:
        message = client.messages.create(
            content="string",
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Altmind) -> None:
        message = client.messages.create(
            content="string",
            message_metadata={},
            original_role="user",
            role="user",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            tool_calls=[{}],
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Altmind) -> None:
        response = client.messages.with_raw_response.create(
            content="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Altmind) -> None:
        with client.messages.with_streaming_response.create(
            content="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(MessageResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Altmind) -> None:
        message = client.messages.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Altmind) -> None:
        response = client.messages.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Altmind) -> None:
        with client.messages.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(MessageResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_id` but received ''"):
            client.messages.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Altmind) -> None:
        message = client.messages.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Altmind) -> None:
        message = client.messages.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            content=[
                {
                    "text": {"value": "value"},
                    "type": "text",
                }
            ],
            message_metadata={},
            role="user",
            tool_calls=[{}],
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Altmind) -> None:
        response = client.messages.with_raw_response.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Altmind) -> None:
        with client.messages.with_streaming_response.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(MessageResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_id` but received ''"):
            client.messages.with_raw_response.update(
                message_id="",
            )

    @parametrize
    def test_method_list(self, client: Altmind) -> None:
        message = client.messages.list()
        assert_matches_type(MessagesResponse, message, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Altmind) -> None:
        message = client.messages.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(MessagesResponse, message, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Altmind) -> None:
        response = client.messages.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(MessagesResponse, message, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Altmind) -> None:
        with client.messages.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(MessagesResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Altmind) -> None:
        message = client.messages.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessageDelete, message, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Altmind) -> None:
        response = client.messages.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(MessageDelete, message, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Altmind) -> None:
        with client.messages.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(MessageDelete, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_id` but received ''"):
            client.messages.with_raw_response.delete(
                "",
            )


class TestAsyncMessages:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.create(
            content="string",
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.create(
            content="string",
            message_metadata={},
            original_role="user",
            role="user",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            tool_calls=[{}],
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAltmind) -> None:
        response = await async_client.messages.with_raw_response.create(
            content="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAltmind) -> None:
        async with async_client.messages.with_streaming_response.create(
            content="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(MessageResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAltmind) -> None:
        response = await async_client.messages.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAltmind) -> None:
        async with async_client.messages.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(MessageResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_id` but received ''"):
            await async_client.messages.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            content=[
                {
                    "text": {"value": "value"},
                    "type": "text",
                }
            ],
            message_metadata={},
            role="user",
            tool_calls=[{}],
        )
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAltmind) -> None:
        response = await async_client.messages.with_raw_response.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(MessageResponse, message, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAltmind) -> None:
        async with async_client.messages.with_streaming_response.update(
            message_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(MessageResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_id` but received ''"):
            await async_client.messages.with_raw_response.update(
                message_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.list()
        assert_matches_type(MessagesResponse, message, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(MessagesResponse, message, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAltmind) -> None:
        response = await async_client.messages.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(MessagesResponse, message, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAltmind) -> None:
        async with async_client.messages.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(MessagesResponse, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAltmind) -> None:
        message = await async_client.messages.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MessageDelete, message, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAltmind) -> None:
        response = await async_client.messages.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(MessageDelete, message, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAltmind) -> None:
        async with async_client.messages.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(MessageDelete, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `message_id` but received ''"):
            await async_client.messages.with_raw_response.delete(
                "",
            )
