# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import login_access_token_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..types.token import Token
from .._base_client import make_request_options
from ..types.shared.user_out import UserOut

__all__ = ["LoginResource", "AsyncLoginResource"]


class LoginResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LoginResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#accessing-raw-response-data-eg-headers
        """
        return LoginResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LoginResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#with_streaming_response
        """
        return LoginResourceWithStreamingResponse(self)

    def access_token(
        self,
        *,
        password: str,
        username: str,
        client_id: Optional[str] | NotGiven = NOT_GIVEN,
        client_secret: Optional[str] | NotGiven = NOT_GIVEN,
        grant_type: Optional[str] | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Token:
        """
        OAuth2 compatible token login, get an access token for future requests

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/login/access-token",
            body=maybe_transform(
                {
                    "password": password,
                    "username": username,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": grant_type,
                    "scope": scope,
                },
                login_access_token_params.LoginAccessTokenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Token,
        )

    def test_token(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """Test access token"""
        return self._post(
            "/api/v1/login/test-token",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )


class AsyncLoginResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLoginResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLoginResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLoginResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#with_streaming_response
        """
        return AsyncLoginResourceWithStreamingResponse(self)

    async def access_token(
        self,
        *,
        password: str,
        username: str,
        client_id: Optional[str] | NotGiven = NOT_GIVEN,
        client_secret: Optional[str] | NotGiven = NOT_GIVEN,
        grant_type: Optional[str] | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Token:
        """
        OAuth2 compatible token login, get an access token for future requests

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/login/access-token",
            body=await async_maybe_transform(
                {
                    "password": password,
                    "username": username,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": grant_type,
                    "scope": scope,
                },
                login_access_token_params.LoginAccessTokenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Token,
        )

    async def test_token(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """Test access token"""
        return await self._post(
            "/api/v1/login/test-token",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )


class LoginResourceWithRawResponse:
    def __init__(self, login: LoginResource) -> None:
        self._login = login

        self.access_token = to_raw_response_wrapper(
            login.access_token,
        )
        self.test_token = to_raw_response_wrapper(
            login.test_token,
        )


class AsyncLoginResourceWithRawResponse:
    def __init__(self, login: AsyncLoginResource) -> None:
        self._login = login

        self.access_token = async_to_raw_response_wrapper(
            login.access_token,
        )
        self.test_token = async_to_raw_response_wrapper(
            login.test_token,
        )


class LoginResourceWithStreamingResponse:
    def __init__(self, login: LoginResource) -> None:
        self._login = login

        self.access_token = to_streamed_response_wrapper(
            login.access_token,
        )
        self.test_token = to_streamed_response_wrapper(
            login.test_token,
        )


class AsyncLoginResourceWithStreamingResponse:
    def __init__(self, login: AsyncLoginResource) -> None:
        self._login = login

        self.access_token = async_to_streamed_response_wrapper(
            login.access_token,
        )
        self.test_token = async_to_streamed_response_wrapper(
            login.test_token,
        )
