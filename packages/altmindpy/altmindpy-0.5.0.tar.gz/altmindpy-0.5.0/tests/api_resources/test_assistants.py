# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from altmindpy import Altmind, AsyncAltmind
from tests.utils import assert_matches_type
from altmindpy.types import (
    AssistantDelete,
    AssistantResponse,
    AssistantsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAssistants:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Altmind) -> None:
        assistant = client.assistants.create(
            model="model",
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Altmind) -> None:
        assistant = client.assistants.create(
            model="model",
            assistant_metadata={},
            description="description",
            instructions="instructions",
            name="name",
            tools=[{}],
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Altmind) -> None:
        response = client.assistants.with_raw_response.create(
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = response.parse()
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Altmind) -> None:
        with client.assistants.with_streaming_response.create(
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = response.parse()
            assert_matches_type(AssistantResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Altmind) -> None:
        assistant = client.assistants.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Altmind) -> None:
        response = client.assistants.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = response.parse()
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Altmind) -> None:
        with client.assistants.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = response.parse()
            assert_matches_type(AssistantResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `assistant_id` but received ''"):
            client.assistants.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Altmind) -> None:
        assistant = client.assistants.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Altmind) -> None:
        assistant = client.assistants.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            assistant_metadata={},
            description="description",
            instructions="instructions",
            model="model",
            name="name",
            tools=[{}],
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Altmind) -> None:
        response = client.assistants.with_raw_response.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = response.parse()
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Altmind) -> None:
        with client.assistants.with_streaming_response.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = response.parse()
            assert_matches_type(AssistantResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `assistant_id` but received ''"):
            client.assistants.with_raw_response.update(
                assistant_id="",
            )

    @parametrize
    def test_method_list(self, client: Altmind) -> None:
        assistant = client.assistants.list()
        assert_matches_type(AssistantsResponse, assistant, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Altmind) -> None:
        assistant = client.assistants.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(AssistantsResponse, assistant, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Altmind) -> None:
        response = client.assistants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = response.parse()
        assert_matches_type(AssistantsResponse, assistant, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Altmind) -> None:
        with client.assistants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = response.parse()
            assert_matches_type(AssistantsResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Altmind) -> None:
        assistant = client.assistants.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AssistantDelete, assistant, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Altmind) -> None:
        response = client.assistants.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = response.parse()
        assert_matches_type(AssistantDelete, assistant, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Altmind) -> None:
        with client.assistants.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = response.parse()
            assert_matches_type(AssistantDelete, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `assistant_id` but received ''"):
            client.assistants.with_raw_response.delete(
                "",
            )


class TestAsyncAssistants:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.create(
            model="model",
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.create(
            model="model",
            assistant_metadata={},
            description="description",
            instructions="instructions",
            name="name",
            tools=[{}],
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAltmind) -> None:
        response = await async_client.assistants.with_raw_response.create(
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = await response.parse()
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAltmind) -> None:
        async with async_client.assistants.with_streaming_response.create(
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = await response.parse()
            assert_matches_type(AssistantResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAltmind) -> None:
        response = await async_client.assistants.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = await response.parse()
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAltmind) -> None:
        async with async_client.assistants.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = await response.parse()
            assert_matches_type(AssistantResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `assistant_id` but received ''"):
            await async_client.assistants.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            assistant_metadata={},
            description="description",
            instructions="instructions",
            model="model",
            name="name",
            tools=[{}],
        )
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAltmind) -> None:
        response = await async_client.assistants.with_raw_response.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = await response.parse()
        assert_matches_type(AssistantResponse, assistant, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAltmind) -> None:
        async with async_client.assistants.with_streaming_response.update(
            assistant_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = await response.parse()
            assert_matches_type(AssistantResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `assistant_id` but received ''"):
            await async_client.assistants.with_raw_response.update(
                assistant_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.list()
        assert_matches_type(AssistantsResponse, assistant, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(AssistantsResponse, assistant, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAltmind) -> None:
        response = await async_client.assistants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = await response.parse()
        assert_matches_type(AssistantsResponse, assistant, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAltmind) -> None:
        async with async_client.assistants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = await response.parse()
            assert_matches_type(AssistantsResponse, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAltmind) -> None:
        assistant = await async_client.assistants.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AssistantDelete, assistant, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAltmind) -> None:
        response = await async_client.assistants.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assistant = await response.parse()
        assert_matches_type(AssistantDelete, assistant, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAltmind) -> None:
        async with async_client.assistants.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assistant = await response.parse()
            assert_matches_type(AssistantDelete, assistant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `assistant_id` but received ''"):
            await async_client.assistants.with_raw_response.delete(
                "",
            )
