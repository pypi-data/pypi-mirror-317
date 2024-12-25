# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from .resources import runs, login, users, threads, assistants, experimental
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import AltmindError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.files import files
from .resources.messages import messages

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Altmind", "AsyncAltmind", "Client", "AsyncClient"]


class Altmind(SyncAPIClient):
    login: login.LoginResource
    users: users.UsersResource
    experimental: experimental.ExperimentalResource
    threads: threads.ThreadsResource
    messages: messages.MessagesResource
    assistants: assistants.AssistantsResource
    runs: runs.RunsResource
    files: files.FilesResource
    with_raw_response: AltmindWithRawResponse
    with_streaming_response: AltmindWithStreamedResponse

    # client options
    access_token: str

    def __init__(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous altmind client instance.

        This automatically infers the `access_token` argument from the `ALTMIND_ACCESS_TOKEN` environment variable if it is not provided.
        """
        if access_token is None:
            access_token = os.environ.get("ALTMIND_ACCESS_TOKEN")
        if access_token is None:
            raise AltmindError(
                "The access_token client option must be set either by passing access_token to the client or by setting the ALTMIND_ACCESS_TOKEN environment variable"
            )
        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("ALTMIND_BASE_URL")
        if base_url is None:
            base_url = f"https://localhost:8000"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.login = login.LoginResource(self)
        self.users = users.UsersResource(self)
        self.experimental = experimental.ExperimentalResource(self)
        self.threads = threads.ThreadsResource(self)
        self.messages = messages.MessagesResource(self)
        self.assistants = assistants.AssistantsResource(self)
        self.runs = runs.RunsResource(self)
        self.files = files.FilesResource(self)
        self.with_raw_response = AltmindWithRawResponse(self)
        self.with_streaming_response = AltmindWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncAltmind(AsyncAPIClient):
    login: login.AsyncLoginResource
    users: users.AsyncUsersResource
    experimental: experimental.AsyncExperimentalResource
    threads: threads.AsyncThreadsResource
    messages: messages.AsyncMessagesResource
    assistants: assistants.AsyncAssistantsResource
    runs: runs.AsyncRunsResource
    files: files.AsyncFilesResource
    with_raw_response: AsyncAltmindWithRawResponse
    with_streaming_response: AsyncAltmindWithStreamedResponse

    # client options
    access_token: str

    def __init__(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async altmind client instance.

        This automatically infers the `access_token` argument from the `ALTMIND_ACCESS_TOKEN` environment variable if it is not provided.
        """
        if access_token is None:
            access_token = os.environ.get("ALTMIND_ACCESS_TOKEN")
        if access_token is None:
            raise AltmindError(
                "The access_token client option must be set either by passing access_token to the client or by setting the ALTMIND_ACCESS_TOKEN environment variable"
            )
        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("ALTMIND_BASE_URL")
        if base_url is None:
            base_url = f"https://localhost:8000"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.login = login.AsyncLoginResource(self)
        self.users = users.AsyncUsersResource(self)
        self.experimental = experimental.AsyncExperimentalResource(self)
        self.threads = threads.AsyncThreadsResource(self)
        self.messages = messages.AsyncMessagesResource(self)
        self.assistants = assistants.AsyncAssistantsResource(self)
        self.runs = runs.AsyncRunsResource(self)
        self.files = files.AsyncFilesResource(self)
        self.with_raw_response = AsyncAltmindWithRawResponse(self)
        self.with_streaming_response = AsyncAltmindWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AltmindWithRawResponse:
    def __init__(self, client: Altmind) -> None:
        self.login = login.LoginResourceWithRawResponse(client.login)
        self.users = users.UsersResourceWithRawResponse(client.users)
        self.experimental = experimental.ExperimentalResourceWithRawResponse(client.experimental)
        self.threads = threads.ThreadsResourceWithRawResponse(client.threads)
        self.messages = messages.MessagesResourceWithRawResponse(client.messages)
        self.assistants = assistants.AssistantsResourceWithRawResponse(client.assistants)
        self.runs = runs.RunsResourceWithRawResponse(client.runs)
        self.files = files.FilesResourceWithRawResponse(client.files)


class AsyncAltmindWithRawResponse:
    def __init__(self, client: AsyncAltmind) -> None:
        self.login = login.AsyncLoginResourceWithRawResponse(client.login)
        self.users = users.AsyncUsersResourceWithRawResponse(client.users)
        self.experimental = experimental.AsyncExperimentalResourceWithRawResponse(client.experimental)
        self.threads = threads.AsyncThreadsResourceWithRawResponse(client.threads)
        self.messages = messages.AsyncMessagesResourceWithRawResponse(client.messages)
        self.assistants = assistants.AsyncAssistantsResourceWithRawResponse(client.assistants)
        self.runs = runs.AsyncRunsResourceWithRawResponse(client.runs)
        self.files = files.AsyncFilesResourceWithRawResponse(client.files)


class AltmindWithStreamedResponse:
    def __init__(self, client: Altmind) -> None:
        self.login = login.LoginResourceWithStreamingResponse(client.login)
        self.users = users.UsersResourceWithStreamingResponse(client.users)
        self.experimental = experimental.ExperimentalResourceWithStreamingResponse(client.experimental)
        self.threads = threads.ThreadsResourceWithStreamingResponse(client.threads)
        self.messages = messages.MessagesResourceWithStreamingResponse(client.messages)
        self.assistants = assistants.AssistantsResourceWithStreamingResponse(client.assistants)
        self.runs = runs.RunsResourceWithStreamingResponse(client.runs)
        self.files = files.FilesResourceWithStreamingResponse(client.files)


class AsyncAltmindWithStreamedResponse:
    def __init__(self, client: AsyncAltmind) -> None:
        self.login = login.AsyncLoginResourceWithStreamingResponse(client.login)
        self.users = users.AsyncUsersResourceWithStreamingResponse(client.users)
        self.experimental = experimental.AsyncExperimentalResourceWithStreamingResponse(client.experimental)
        self.threads = threads.AsyncThreadsResourceWithStreamingResponse(client.threads)
        self.messages = messages.AsyncMessagesResourceWithStreamingResponse(client.messages)
        self.assistants = assistants.AsyncAssistantsResourceWithStreamingResponse(client.assistants)
        self.runs = runs.AsyncRunsResourceWithStreamingResponse(client.runs)
        self.files = files.AsyncFilesResourceWithStreamingResponse(client.files)


Client = Altmind

AsyncClient = AsyncAltmind
