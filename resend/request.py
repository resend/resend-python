from typing import Any, Dict, Generic, List, Optional, Union, cast

import requests
import json
from typing_extensions import Literal, TypeVar

import resend
from resend.exceptions import NoContentError, raise_for_code_and_type
from resend.version import get_version

RequestVerb = Literal["get", "post", "put", "patch", "delete"]

T = TypeVar("T")


# This class wraps the HTTP request creation logic
class Request(Generic[T]):
    def __init__(
        self,
        path: str,
        params: Union[Dict[Any, Any], List[Dict[Any, Any]]],
        verb: RequestVerb,
        options: Optional[Dict[str, Any]] = None,
    ):
        self.path = path
        self.params = params
        self.verb = verb
        self.options = options

    def perform(self) -> Union[T, None]:
        data = self.make_request(url=f"{resend.api_url}{self.path}")

        if self.verb == "delete":
            return None

        if (
            isinstance(data, dict)
            and data.get("statusCode")
            and data.get("statusCode") != 200
        ):
            raise_for_code_and_type(
                code=data.get("statusCode") or 500,
                message=data.get("message", "Unknown error"),
                error_type=data.get("name", "InternalServerError"),
            )

        return cast(T, data)

    def perform_with_content(self) -> T:
        """
        Perform an HTTP request and return the response content.

        Returns:
            T: The content of the response

        Raises:
            NoContentError: If the response content is `None`.
        """
        resp = self.perform()
        if resp is None:
            raise NoContentError()
        return resp

    def __get_headers(self) -> Dict[Any, Any]:
        """get_headers returns the HTTP headers that will be
        used for every req.

        Returns:
            Dict: configured HTTP Headers
        """
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {resend.api_key}",
            "User-Agent": f"resend-python:{get_version()}",
        }

        # Add the Idempotency-Key header if the verb is POST
        # and the options dict contains the key
        if self.verb == "post" and (self.options and "idempotency_key" in self.options):
            headers["Idempotency-Key"] = self.options["idempotency_key"]
        return headers

    def make_request(self, url: str) -> Dict[str, Any]:
        headers = self.__get_headers()

        content, status_code, resp_headers = resend.default_http_client.request(
            method=self.verb,
            url=url,
            headers=headers,
            json=self.params,
        )

        content_type = resp_headers.get("Content-Type", "")

        if "application/json" not in content_type:
            raise_for_code_and_type(
                code=500,
                message="Expected JSON response but got: " + content_type,
                error_type="InternalServerError",
            )

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise_for_code_and_type(
                code=500,
                message="Failed to decode JSON response",
                error_type="InternalServerError",
            )
