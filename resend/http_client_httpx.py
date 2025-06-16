from typing import Dict, List, Mapping, Optional, Tuple, Union

from resend.http_client_async import AsyncHTTPClient

try:
    import httpx
except ImportError:
    raise ImportError(
        "httpx is required for async support. Install it with: pip install resend[async]"
    )


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
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json,
                )
                return resp.content, resp.status_code, resp.headers
        except httpx.RequestError as e:
            # This gets caught by the async request.perform() method
            # and raises a ResendError with the error type "HttpClientError"
            raise RuntimeError(f"Request failed: {e}") from e