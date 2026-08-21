import asyncio
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

import httpx

from resend.http_client_async import AsyncHTTPClient


class HTTPXClient(AsyncHTTPClient):
    """
    Async HTTP client implementation using the httpx library.

    The client holds a single :class:`httpx.AsyncClient` so that the underlying
    TCP connection (and its TLS handshake) is reused across requests.

    The underlying client is created lazily on first use rather than in
    ``__init__``, because an ``httpx.AsyncClient`` binds its connection pool to
    the running event loop and this class is instantiated at import time, when
    no loop is running. If the running loop changes (for example, a second
    ``asyncio.run(...)`` call), a fresh client is created for the new loop.

    Call :meth:`aclose` when the client is no longer needed.
    """

    def __init__(self, timeout: int = 30):
        self._timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def _get_client(self) -> httpx.AsyncClient:
        loop = asyncio.get_running_loop()

        if self._client is None or self._client.is_closed or self._loop is not loop:
            # A client bound to a previous loop cannot be awaited on this one,
            # and its pooled connections died with that loop, so it is dropped
            # rather than closed here.
            self._client = httpx.AsyncClient(timeout=self._timeout)
            self._loop = loop

        return self._client

    async def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[Dict[str, object], List[object]]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, str]] = None,
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        client = self._get_client()

        try:
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
        except httpx.RequestError as e:
            # This gets caught by the async request.perform() method
            # and raises a ResendError with the error type "HttpClientError"
            raise RuntimeError(f"Request failed: {e}") from e

    async def aclose(self) -> None:
        """Close the underlying client and release pooled connections."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
        self._client = None
        self._loop = None
