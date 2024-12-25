# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from altmindpy import Altmind, AsyncAltmind
from tests.utils import assert_matches_type
from altmindpy.types import Token
from altmindpy.types.shared import UserOut

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLogin:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_access_token(self, client: Altmind) -> None:
        login = client.login.access_token(
            password="password",
            username="username",
        )
        assert_matches_type(Token, login, path=["response"])

    @parametrize
    def test_method_access_token_with_all_params(self, client: Altmind) -> None:
        login = client.login.access_token(
            password="password",
            username="username",
            client_id="client_id",
            client_secret="client_secret",
            grant_type="grant_type",
            scope="scope",
        )
        assert_matches_type(Token, login, path=["response"])

    @parametrize
    def test_raw_response_access_token(self, client: Altmind) -> None:
        response = client.login.with_raw_response.access_token(
            password="password",
            username="username",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        login = response.parse()
        assert_matches_type(Token, login, path=["response"])

    @parametrize
    def test_streaming_response_access_token(self, client: Altmind) -> None:
        with client.login.with_streaming_response.access_token(
            password="password",
            username="username",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            login = response.parse()
            assert_matches_type(Token, login, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_test_token(self, client: Altmind) -> None:
        login = client.login.test_token()
        assert_matches_type(UserOut, login, path=["response"])

    @parametrize
    def test_raw_response_test_token(self, client: Altmind) -> None:
        response = client.login.with_raw_response.test_token()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        login = response.parse()
        assert_matches_type(UserOut, login, path=["response"])

    @parametrize
    def test_streaming_response_test_token(self, client: Altmind) -> None:
        with client.login.with_streaming_response.test_token() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            login = response.parse()
            assert_matches_type(UserOut, login, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLogin:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_access_token(self, async_client: AsyncAltmind) -> None:
        login = await async_client.login.access_token(
            password="password",
            username="username",
        )
        assert_matches_type(Token, login, path=["response"])

    @parametrize
    async def test_method_access_token_with_all_params(self, async_client: AsyncAltmind) -> None:
        login = await async_client.login.access_token(
            password="password",
            username="username",
            client_id="client_id",
            client_secret="client_secret",
            grant_type="grant_type",
            scope="scope",
        )
        assert_matches_type(Token, login, path=["response"])

    @parametrize
    async def test_raw_response_access_token(self, async_client: AsyncAltmind) -> None:
        response = await async_client.login.with_raw_response.access_token(
            password="password",
            username="username",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        login = await response.parse()
        assert_matches_type(Token, login, path=["response"])

    @parametrize
    async def test_streaming_response_access_token(self, async_client: AsyncAltmind) -> None:
        async with async_client.login.with_streaming_response.access_token(
            password="password",
            username="username",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            login = await response.parse()
            assert_matches_type(Token, login, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_test_token(self, async_client: AsyncAltmind) -> None:
        login = await async_client.login.test_token()
        assert_matches_type(UserOut, login, path=["response"])

    @parametrize
    async def test_raw_response_test_token(self, async_client: AsyncAltmind) -> None:
        response = await async_client.login.with_raw_response.test_token()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        login = await response.parse()
        assert_matches_type(UserOut, login, path=["response"])

    @parametrize
    async def test_streaming_response_test_token(self, async_client: AsyncAltmind) -> None:
        async with async_client.login.with_streaming_response.test_token() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            login = await response.parse()
            assert_matches_type(UserOut, login, path=["response"])

        assert cast(Any, response.is_closed) is True
