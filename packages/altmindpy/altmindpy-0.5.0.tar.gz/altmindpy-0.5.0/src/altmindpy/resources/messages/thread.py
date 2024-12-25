# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.messages import thread_list_params
from ...types.messages_response import MessagesResponse

__all__ = ["ThreadResource", "AsyncThreadResource"]


class ThreadResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ThreadResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#accessing-raw-response-data-eg-headers
        """
        return ThreadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ThreadResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#with_streaming_response
        """
        return ThreadResourceWithStreamingResponse(self)

    def list(
        self,
        thread_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MessagesResponse:
        """
        Retrieve messages by thread ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._get(
            f"/api/v1/messages/thread/{thread_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    thread_list_params.ThreadListParams,
                ),
            ),
            cast_to=MessagesResponse,
        )


class AsyncThreadResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncThreadResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#accessing-raw-response-data-eg-headers
        """
        return AsyncThreadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncThreadResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/AltermindLabs/altmind-python#with_streaming_response
        """
        return AsyncThreadResourceWithStreamingResponse(self)

    async def list(
        self,
        thread_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MessagesResponse:
        """
        Retrieve messages by thread ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._get(
            f"/api/v1/messages/thread/{thread_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    thread_list_params.ThreadListParams,
                ),
            ),
            cast_to=MessagesResponse,
        )


class ThreadResourceWithRawResponse:
    def __init__(self, thread: ThreadResource) -> None:
        self._thread = thread

        self.list = to_raw_response_wrapper(
            thread.list,
        )


class AsyncThreadResourceWithRawResponse:
    def __init__(self, thread: AsyncThreadResource) -> None:
        self._thread = thread

        self.list = async_to_raw_response_wrapper(
            thread.list,
        )


class ThreadResourceWithStreamingResponse:
    def __init__(self, thread: ThreadResource) -> None:
        self._thread = thread

        self.list = to_streamed_response_wrapper(
            thread.list,
        )


class AsyncThreadResourceWithStreamingResponse:
    def __init__(self, thread: AsyncThreadResource) -> None:
        self._thread = thread

        self.list = async_to_streamed_response_wrapper(
            thread.list,
        )
