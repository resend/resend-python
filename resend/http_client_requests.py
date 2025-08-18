from typing import Dict, List, Mapping, Optional, Tuple, Union

import requests

from resend.http_client import HTTPClient


class RequestsClient(HTTPClient):
    """
    This is the default HTTP client implementation using the requests library.
    """

    def __init__(self, timeout: int = 30):
        self._timeout = timeout

    def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[Dict[str, object], List[object]]] = None,
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        try:
            resp = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json,
                timeout=self._timeout,
            )
            return resp.content, resp.status_code, resp.headers
        except requests.RequestException as e:
            # This gets caught by the request.perform() method
            # and raises a ResendError with the error type "HttpClientError"
            raise RuntimeError(f"Request failed: {e}") from e
