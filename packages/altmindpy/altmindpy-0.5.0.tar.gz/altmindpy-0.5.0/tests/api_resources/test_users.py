# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from altmindpy import Altmind, AsyncAltmind
from tests.utils import assert_matches_type
from altmindpy.types import (
    UsersOut,
    ResponseMessage,
)
from altmindpy.types.shared import UserOut

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Altmind) -> None:
        user = client.users.create(
            email="email",
            password="password",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Altmind) -> None:
        user = client.users.create(
            email="email",
            password="password",
            full_name="full_name",
            is_active=True,
            is_superuser=True,
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Altmind) -> None:
        response = client.users.with_raw_response.create(
            email="email",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Altmind) -> None:
        with client.users.with_streaming_response.create(
            email="email",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Altmind) -> None:
        user = client.users.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Altmind) -> None:
        response = client.users.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Altmind) -> None:
        with client.users.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Altmind) -> None:
        user = client.users.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Altmind) -> None:
        user = client.users.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="email",
            full_name="full_name",
            is_active=True,
            is_superuser=True,
            password="password",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Altmind) -> None:
        response = client.users.with_raw_response.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Altmind) -> None:
        with client.users.with_streaming_response.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.update(
                user_id="",
            )

    @parametrize
    def test_method_list(self, client: Altmind) -> None:
        user = client.users.list()
        assert_matches_type(UsersOut, user, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Altmind) -> None:
        user = client.users.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(UsersOut, user, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Altmind) -> None:
        response = client.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UsersOut, user, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Altmind) -> None:
        with client.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UsersOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Altmind) -> None:
        user = client.users.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Altmind) -> None:
        response = client.users.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Altmind) -> None:
        with client.users.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(ResponseMessage, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Altmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_open(self, client: Altmind) -> None:
        user = client.users.open(
            email="email",
            password="password",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_method_open_with_all_params(self, client: Altmind) -> None:
        user = client.users.open(
            email="email",
            password="password",
            full_name="full_name",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_raw_response_open(self, client: Altmind) -> None:
        response = client.users.with_raw_response.open(
            email="email",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    def test_streaming_response_open(self, client: Altmind) -> None:
        with client.users.with_streaming_response.open(
            email="email",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_password(self, client: Altmind) -> None:
        user = client.users.password(
            current_password="current_password",
            new_password="new_password",
        )
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    def test_raw_response_password(self, client: Altmind) -> None:
        response = client.users.with_raw_response.password(
            current_password="current_password",
            new_password="new_password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    def test_streaming_response_password(self, client: Altmind) -> None:
        with client.users.with_streaming_response.password(
            current_password="current_password",
            new_password="new_password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(ResponseMessage, user, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.create(
            email="email",
            password="password",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.create(
            email="email",
            password="password",
            full_name="full_name",
            is_active=True,
            is_superuser=True,
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAltmind) -> None:
        response = await async_client.users.with_raw_response.create(
            email="email",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAltmind) -> None:
        async with async_client.users.with_streaming_response.create(
            email="email",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAltmind) -> None:
        response = await async_client.users.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAltmind) -> None:
        async with async_client.users.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="email",
            full_name="full_name",
            is_active=True,
            is_superuser=True,
            password="password",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAltmind) -> None:
        response = await async_client.users.with_raw_response.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAltmind) -> None:
        async with async_client.users.with_streaming_response.update(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.update(
                user_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.list()
        assert_matches_type(UsersOut, user, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(UsersOut, user, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAltmind) -> None:
        response = await async_client.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UsersOut, user, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAltmind) -> None:
        async with async_client.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UsersOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAltmind) -> None:
        response = await async_client.users.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAltmind) -> None:
        async with async_client.users.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(ResponseMessage, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAltmind) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_open(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.open(
            email="email",
            password="password",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_method_open_with_all_params(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.open(
            email="email",
            password="password",
            full_name="full_name",
        )
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_raw_response_open(self, async_client: AsyncAltmind) -> None:
        response = await async_client.users.with_raw_response.open(
            email="email",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserOut, user, path=["response"])

    @parametrize
    async def test_streaming_response_open(self, async_client: AsyncAltmind) -> None:
        async with async_client.users.with_streaming_response.open(
            email="email",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserOut, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_password(self, async_client: AsyncAltmind) -> None:
        user = await async_client.users.password(
            current_password="current_password",
            new_password="new_password",
        )
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    async def test_raw_response_password(self, async_client: AsyncAltmind) -> None:
        response = await async_client.users.with_raw_response.password(
            current_password="current_password",
            new_password="new_password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(ResponseMessage, user, path=["response"])

    @parametrize
    async def test_streaming_response_password(self, async_client: AsyncAltmind) -> None:
        async with async_client.users.with_streaming_response.password(
            current_password="current_password",
            new_password="new_password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(ResponseMessage, user, path=["response"])

        assert cast(Any, response.is_closed) is True
