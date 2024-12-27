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
from .resources import tokens, schemas, outlines, snapshots, reports_v3, collections, created_fields, prompt_templates
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import EvrimError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.bulk import bulk
from .resources.tags import tags
from .resources.blank import blank
from .resources.profiles import profiles
from .resources.templates import templates

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Evrim", "AsyncEvrim", "Client", "AsyncClient"]


class Evrim(SyncAPIClient):
    blank: blank.BlankResource
    bulk: bulk.BulkResource
    collections: collections.CollectionsResource
    created_fields: created_fields.CreatedFieldsResource
    outlines: outlines.OutlinesResource
    profiles: profiles.ProfilesResource
    prompt_templates: prompt_templates.PromptTemplatesResource
    reports_v3: reports_v3.ReportsV3Resource
    schemas: schemas.SchemasResource
    snapshots: snapshots.SnapshotsResource
    tags: tags.TagsResource
    templates: templates.TemplatesResource
    tokens: tokens.TokensResource
    with_raw_response: EvrimWithRawResponse
    with_streaming_response: EvrimWithStreamedResponse

    # client options
    jwt_access_token: str
    session_id: str

    def __init__(
        self,
        *,
        jwt_access_token: str | None = None,
        session_id: str | None = None,
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
        """Construct a new synchronous evrim client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `jwt_access_token` from `JWT_ACCESS_TOKEN`
        - `session_id` from `SESSION_ID`
        """
        if jwt_access_token is None:
            jwt_access_token = os.environ.get("JWT_ACCESS_TOKEN")
        if jwt_access_token is None:
            raise EvrimError(
                "The jwt_access_token client option must be set either by passing jwt_access_token to the client or by setting the JWT_ACCESS_TOKEN environment variable"
            )
        self.jwt_access_token = jwt_access_token

        if session_id is None:
            session_id = os.environ.get("SESSION_ID")
        if session_id is None:
            raise EvrimError(
                "The session_id client option must be set either by passing session_id to the client or by setting the SESSION_ID environment variable"
            )
        self.session_id = session_id

        if base_url is None:
            base_url = os.environ.get("EVRIM_BASE_URL")
        if base_url is None:
            base_url = f"https://localhost:8080/test-api"

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

        self.blank = blank.BlankResource(self)
        self.bulk = bulk.BulkResource(self)
        self.collections = collections.CollectionsResource(self)
        self.created_fields = created_fields.CreatedFieldsResource(self)
        self.outlines = outlines.OutlinesResource(self)
        self.profiles = profiles.ProfilesResource(self)
        self.prompt_templates = prompt_templates.PromptTemplatesResource(self)
        self.reports_v3 = reports_v3.ReportsV3Resource(self)
        self.schemas = schemas.SchemasResource(self)
        self.snapshots = snapshots.SnapshotsResource(self)
        self.tags = tags.TagsResource(self)
        self.templates = templates.TemplatesResource(self)
        self.tokens = tokens.TokensResource(self)
        self.with_raw_response = EvrimWithRawResponse(self)
        self.with_streaming_response = EvrimWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._cookie_auth:
            return self._cookie_auth
        if self._jwt_auth:
            return self._jwt_auth
        return {}

    @property
    def _cookie_auth(self) -> dict[str, str]:
        session_id = self.session_id
        return {"sessionid": session_id}

    @property
    def _jwt_auth(self) -> dict[str, str]:
        jwt_access_token = self.jwt_access_token
        return {"Authorization": f"Bearer {jwt_access_token}"}

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
        jwt_access_token: str | None = None,
        session_id: str | None = None,
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
            jwt_access_token=jwt_access_token or self.jwt_access_token,
            session_id=session_id or self.session_id,
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


class AsyncEvrim(AsyncAPIClient):
    blank: blank.AsyncBlankResource
    bulk: bulk.AsyncBulkResource
    collections: collections.AsyncCollectionsResource
    created_fields: created_fields.AsyncCreatedFieldsResource
    outlines: outlines.AsyncOutlinesResource
    profiles: profiles.AsyncProfilesResource
    prompt_templates: prompt_templates.AsyncPromptTemplatesResource
    reports_v3: reports_v3.AsyncReportsV3Resource
    schemas: schemas.AsyncSchemasResource
    snapshots: snapshots.AsyncSnapshotsResource
    tags: tags.AsyncTagsResource
    templates: templates.AsyncTemplatesResource
    tokens: tokens.AsyncTokensResource
    with_raw_response: AsyncEvrimWithRawResponse
    with_streaming_response: AsyncEvrimWithStreamedResponse

    # client options
    jwt_access_token: str
    session_id: str

    def __init__(
        self,
        *,
        jwt_access_token: str | None = None,
        session_id: str | None = None,
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
        """Construct a new async evrim client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `jwt_access_token` from `JWT_ACCESS_TOKEN`
        - `session_id` from `SESSION_ID`
        """
        if jwt_access_token is None:
            jwt_access_token = os.environ.get("JWT_ACCESS_TOKEN")
        if jwt_access_token is None:
            raise EvrimError(
                "The jwt_access_token client option must be set either by passing jwt_access_token to the client or by setting the JWT_ACCESS_TOKEN environment variable"
            )
        self.jwt_access_token = jwt_access_token

        if session_id is None:
            session_id = os.environ.get("SESSION_ID")
        if session_id is None:
            raise EvrimError(
                "The session_id client option must be set either by passing session_id to the client or by setting the SESSION_ID environment variable"
            )
        self.session_id = session_id

        if base_url is None:
            base_url = os.environ.get("EVRIM_BASE_URL")
        if base_url is None:
            base_url = f"https://localhost:8080/test-api"

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

        self.blank = blank.AsyncBlankResource(self)
        self.bulk = bulk.AsyncBulkResource(self)
        self.collections = collections.AsyncCollectionsResource(self)
        self.created_fields = created_fields.AsyncCreatedFieldsResource(self)
        self.outlines = outlines.AsyncOutlinesResource(self)
        self.profiles = profiles.AsyncProfilesResource(self)
        self.prompt_templates = prompt_templates.AsyncPromptTemplatesResource(self)
        self.reports_v3 = reports_v3.AsyncReportsV3Resource(self)
        self.schemas = schemas.AsyncSchemasResource(self)
        self.snapshots = snapshots.AsyncSnapshotsResource(self)
        self.tags = tags.AsyncTagsResource(self)
        self.templates = templates.AsyncTemplatesResource(self)
        self.tokens = tokens.AsyncTokensResource(self)
        self.with_raw_response = AsyncEvrimWithRawResponse(self)
        self.with_streaming_response = AsyncEvrimWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._cookie_auth:
            return self._cookie_auth
        if self._jwt_auth:
            return self._jwt_auth
        return {}

    @property
    def _cookie_auth(self) -> dict[str, str]:
        session_id = self.session_id
        return {"sessionid": session_id}

    @property
    def _jwt_auth(self) -> dict[str, str]:
        jwt_access_token = self.jwt_access_token
        return {"Authorization": f"Bearer {jwt_access_token}"}

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
        jwt_access_token: str | None = None,
        session_id: str | None = None,
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
            jwt_access_token=jwt_access_token or self.jwt_access_token,
            session_id=session_id or self.session_id,
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


class EvrimWithRawResponse:
    def __init__(self, client: Evrim) -> None:
        self.blank = blank.BlankResourceWithRawResponse(client.blank)
        self.bulk = bulk.BulkResourceWithRawResponse(client.bulk)
        self.collections = collections.CollectionsResourceWithRawResponse(client.collections)
        self.created_fields = created_fields.CreatedFieldsResourceWithRawResponse(client.created_fields)
        self.outlines = outlines.OutlinesResourceWithRawResponse(client.outlines)
        self.profiles = profiles.ProfilesResourceWithRawResponse(client.profiles)
        self.prompt_templates = prompt_templates.PromptTemplatesResourceWithRawResponse(client.prompt_templates)
        self.reports_v3 = reports_v3.ReportsV3ResourceWithRawResponse(client.reports_v3)
        self.schemas = schemas.SchemasResourceWithRawResponse(client.schemas)
        self.snapshots = snapshots.SnapshotsResourceWithRawResponse(client.snapshots)
        self.tags = tags.TagsResourceWithRawResponse(client.tags)
        self.templates = templates.TemplatesResourceWithRawResponse(client.templates)
        self.tokens = tokens.TokensResourceWithRawResponse(client.tokens)


class AsyncEvrimWithRawResponse:
    def __init__(self, client: AsyncEvrim) -> None:
        self.blank = blank.AsyncBlankResourceWithRawResponse(client.blank)
        self.bulk = bulk.AsyncBulkResourceWithRawResponse(client.bulk)
        self.collections = collections.AsyncCollectionsResourceWithRawResponse(client.collections)
        self.created_fields = created_fields.AsyncCreatedFieldsResourceWithRawResponse(client.created_fields)
        self.outlines = outlines.AsyncOutlinesResourceWithRawResponse(client.outlines)
        self.profiles = profiles.AsyncProfilesResourceWithRawResponse(client.profiles)
        self.prompt_templates = prompt_templates.AsyncPromptTemplatesResourceWithRawResponse(client.prompt_templates)
        self.reports_v3 = reports_v3.AsyncReportsV3ResourceWithRawResponse(client.reports_v3)
        self.schemas = schemas.AsyncSchemasResourceWithRawResponse(client.schemas)
        self.snapshots = snapshots.AsyncSnapshotsResourceWithRawResponse(client.snapshots)
        self.tags = tags.AsyncTagsResourceWithRawResponse(client.tags)
        self.templates = templates.AsyncTemplatesResourceWithRawResponse(client.templates)
        self.tokens = tokens.AsyncTokensResourceWithRawResponse(client.tokens)


class EvrimWithStreamedResponse:
    def __init__(self, client: Evrim) -> None:
        self.blank = blank.BlankResourceWithStreamingResponse(client.blank)
        self.bulk = bulk.BulkResourceWithStreamingResponse(client.bulk)
        self.collections = collections.CollectionsResourceWithStreamingResponse(client.collections)
        self.created_fields = created_fields.CreatedFieldsResourceWithStreamingResponse(client.created_fields)
        self.outlines = outlines.OutlinesResourceWithStreamingResponse(client.outlines)
        self.profiles = profiles.ProfilesResourceWithStreamingResponse(client.profiles)
        self.prompt_templates = prompt_templates.PromptTemplatesResourceWithStreamingResponse(client.prompt_templates)
        self.reports_v3 = reports_v3.ReportsV3ResourceWithStreamingResponse(client.reports_v3)
        self.schemas = schemas.SchemasResourceWithStreamingResponse(client.schemas)
        self.snapshots = snapshots.SnapshotsResourceWithStreamingResponse(client.snapshots)
        self.tags = tags.TagsResourceWithStreamingResponse(client.tags)
        self.templates = templates.TemplatesResourceWithStreamingResponse(client.templates)
        self.tokens = tokens.TokensResourceWithStreamingResponse(client.tokens)


class AsyncEvrimWithStreamedResponse:
    def __init__(self, client: AsyncEvrim) -> None:
        self.blank = blank.AsyncBlankResourceWithStreamingResponse(client.blank)
        self.bulk = bulk.AsyncBulkResourceWithStreamingResponse(client.bulk)
        self.collections = collections.AsyncCollectionsResourceWithStreamingResponse(client.collections)
        self.created_fields = created_fields.AsyncCreatedFieldsResourceWithStreamingResponse(client.created_fields)
        self.outlines = outlines.AsyncOutlinesResourceWithStreamingResponse(client.outlines)
        self.profiles = profiles.AsyncProfilesResourceWithStreamingResponse(client.profiles)
        self.prompt_templates = prompt_templates.AsyncPromptTemplatesResourceWithStreamingResponse(
            client.prompt_templates
        )
        self.reports_v3 = reports_v3.AsyncReportsV3ResourceWithStreamingResponse(client.reports_v3)
        self.schemas = schemas.AsyncSchemasResourceWithStreamingResponse(client.schemas)
        self.snapshots = snapshots.AsyncSnapshotsResourceWithStreamingResponse(client.snapshots)
        self.tags = tags.AsyncTagsResourceWithStreamingResponse(client.tags)
        self.templates = templates.AsyncTemplatesResourceWithStreamingResponse(client.templates)
        self.tokens = tokens.AsyncTokensResourceWithStreamingResponse(client.tokens)


Client = Evrim

AsyncClient = AsyncEvrim
