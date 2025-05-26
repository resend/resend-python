from typing import Mapping, Optional, Tuple, Union

import requests

from resend.http_client import HTTPClient


class RequestsClient(HTTPClient):
    def __init__(self, timeout: int = 30):
        self._timeout = timeout

    def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[dict, list]] = None,
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
            raise RuntimeError(f"Request failed: {e}") from e
