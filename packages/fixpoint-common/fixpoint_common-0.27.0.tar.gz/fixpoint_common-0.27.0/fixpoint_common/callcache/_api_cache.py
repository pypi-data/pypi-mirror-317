"""A callcache that uses the Fixpoint API as a backend"""

__all__ = ["StepApiCallCache", "TaskApiCallCache"]

import json
from typing import Any, Optional, Type

import httpx

from fixpoint_common.constants import DEFAULT_API_CLIENT_TIMEOUT
from fixpoint_common.config import get_env_api_url
from fixpoint_common.types.callcache import (
    CreateCallcacheEntryRequest,
    GetCallcacheEntryRequest,
    CacheEntry,
)
from fixpoint_common.utils.http import route_url, new_api_key_http_header
from ._shared import (
    CallCache,
    CallCacheKind,
    CacheResult,
    deserialize_json_val,
    default_json_dumps,
)


class _BaseApiCallCache(CallCache):
    cache_kind: CallCacheKind

    _api_key: str
    _api_url: str
    _http_client: httpx.Client
    _async_http_client: httpx.AsyncClient

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
    ):
        self._api_key = api_key
        if api_url is None:
            api_url = get_env_api_url()
        self._api_url = api_url

        if http_client:
            self._http_client = http_client
        else:
            self._http_client = httpx.Client(timeout=DEFAULT_API_CLIENT_TIMEOUT)

        if async_http_client:
            self._async_http_client = async_http_client
        else:
            self._async_http_client = httpx.AsyncClient(
                timeout=DEFAULT_API_CLIENT_TIMEOUT
            )
        self._http_client.headers.update(new_api_key_http_header(self._api_key))
        self._async_http_client.headers.update(new_api_key_http_header(self._api_key))

    def check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        # org ID is ignored because we pull that from the API key
        response = self._http_client.get(
            route_url(
                self._api_url,
                "callcache",
                run_id,
                self.cache_kind.value,
                kind_id,
                serialized_args,
            )
        )
        response.raise_for_status()
        return _parse_check_response(response, type_hint)

    def store_result(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        res: Any,
        ttl_s: Optional[float] = None,
    ) -> None:
        """Store the result of a task or step call"""
        if ttl_s is not None:
            raise ValueError("ttl_s is not supported for API call-cache")
        # org ID is ignored because we pull that from the API key
        resp = self._http_client.post(
            route_url(
                self._api_url, "callcache", run_id, self.cache_kind.value, kind_id
            ),
            json=CreateCallcacheEntryRequest(
                cache_key=serialized_args,
                result=default_json_dumps(res),
            ).model_dump(),
        )
        resp.raise_for_status()

    async def async_check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        # org ID is ignored because we pull that from the API key
        response = await self._async_http_client.post(
            route_url(
                self._api_url,
                "callcache",
                run_id,
                self.cache_kind.value,
                f"{kind_id}:get_cache_entry",
            ),
            json=GetCallcacheEntryRequest(
                cache_key=serialized_args,
            ).model_dump(),
        )
        response.raise_for_status()
        return _parse_check_response(response, type_hint)

    async def async_store_result(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        res: Any,
        ttl_s: Optional[float] = None,
    ) -> None:
        if ttl_s is not None:
            raise ValueError("ttl_s is not supported for API call-cache")
        # org ID is ignored because we pull that from the API key
        resp = await self._async_http_client.post(
            route_url(
                self._api_url, "callcache", run_id, self.cache_kind.value, kind_id
            ),
            json=CreateCallcacheEntryRequest(
                cache_key=serialized_args,
                result=default_json_dumps(res),
            ).model_dump(),
        )
        resp.raise_for_status()


class StepApiCallCache(_BaseApiCallCache):
    """A step callcache that uses the Fixpoint API as a backend"""

    cache_kind = CallCacheKind.STEP


class TaskApiCallCache(_BaseApiCallCache):
    """A task callcache that uses the Fixpoint API as a backend"""

    cache_kind = CallCacheKind.TASK


def _parse_check_response(
    response: httpx.Response, type_hint: Optional[Type[Any]] = None
) -> CacheResult[Any]:
    cache_entry = CacheEntry.model_validate(response.json())
    # Do these explicit checks so that type narrowing can narrow the
    # cache_entry.result down to the right union type
    if not cache_entry.found:
        return CacheResult[Any](
            found=False,
            result=None,
        )
    if cache_entry.result is None:
        return CacheResult[Any](
            found=True,
            result=None,
        )
    # Because the cached values are serialized to JSON strings when they are
    # sent to the API server, when we get them back we need to deserialize them.
    res = json.loads(cache_entry.result)
    return CacheResult[Any](
        found=cache_entry.found,
        result=deserialize_json_val(res, type_hint),
    )
