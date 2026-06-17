from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

import httpx

from resend.http_client_async import AsyncHTTPClient


class HTTPXClient(AsyncHTTPClient):
    """
    Async HTTP client implementation using the httpx library.
    """

    def __init__(self, timeout: int = 30):
        self._timeout = timeout

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
            async with httpx.AsyncClient(timeout=self._timeout) as client:
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
