from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

import httpx

from resend.http_client_async import AsyncHTTPClient


class HTTPXClient(AsyncHTTPClient):
    """
    Async HTTP client implementation using the httpx library.

    Pass an ``httpx.AsyncClient`` as ``client`` to reuse its connections across
    requests. The caller owns that client and is responsible for closing it.
    """

    def __init__(self, timeout: int = 30, client: Optional[httpx.AsyncClient] = None):
        self._timeout = timeout
        self._client = client

    async def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[Dict[str, object], List[object]]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, str]] = None,
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        try:
            if self._client is not None:
                return await self._send(
                    self._client, method, url, headers, json, files, data
                )
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                return await self._send(client, method, url, headers, json, files, data)
        except httpx.RequestError as e:
            # This gets caught by the async request.perform() method
            # and raises a ResendError with the error type "HttpClientError"
            raise RuntimeError(f"Request failed: {e}") from e

    async def _send(
        self,
        client: httpx.AsyncClient,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[Dict[str, object], List[object]]],
        files: Optional[Dict[str, Any]],
        data: Optional[Dict[str, str]],
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        if files is not None:
            resp = await client.request(
                method=method,
                url=url,
                headers=headers,
                files=files,
                data=data,
            )
        else:
            resp = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=json if data is None else None,
                data=data,
            )
        return resp.content, resp.status_code, resp.headers
