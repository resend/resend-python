import os
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

import requests

import resend
from resend.http_client import HTTPClient

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


# Define a custom HTTP client using the requests library with a higher timeout val
class CustomRequestsClient(HTTPClient):
    def __init__(self, timeout: int = 300):
        self.timeout = timeout

    def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[Dict[str, Any], List[Any]]] = None,
    ) -> Tuple[bytes, int, Dict[str, str]]:
        print(f"[HTTP] {method.upper()} {url} with timeout={self.timeout}")
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json,
                timeout=self.timeout,
            )
            return (
                response.content,
                response.status_code,
                dict(response.headers),
            )
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}") from e


# use the custom HTTP client with a longer timeout
resend.default_http_client = CustomRequestsClient(timeout=400)

params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hi",
    "html": "<strong>hello, world!</strong>",
    "reply_to": "to@gmail.com",
    "bcc": "delivered@resend.dev",
    "cc": ["delivered@resend.dev"],
    "tags": [
        {"name": "tag1", "value": "tagvalue1"},
        {"name": "tag2", "value": "tagvalue2"},
    ],
}


email: resend.Email = resend.Emails.send(params)
print(f"{email}")
