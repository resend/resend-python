import json
from typing import Any, Dict, Generic, List, Optional, Union, cast

from typing_extensions import Literal, TypeVar

import resend
from resend.exceptions import (NoContentError, ResendError,
                               raise_for_code_and_type)
from resend.version import get_version

RequestVerb = Literal["get", "post", "put", "patch", "delete"]
T = TypeVar("T")

ParamsType = Union[Dict[str, Any], List[Dict[str, Any]]]
HeadersType = Dict[str, str]


class Request(Generic[T]):
    def __init__(
        self,
        path: str,
        params: ParamsType,
        verb: RequestVerb,
        options: Optional[Dict[str, Any]] = None,
    ):
        self.path = path
        self.params = params
        self.verb = verb
        self.options = options

    def perform(self) -> Union[T, None]:
        data = self.make_request(url=f"{resend.api_url}{self.path}")

        if isinstance(data, dict) and data.get("statusCode") not in (None, 200):
            raise_for_code_and_type(
                code=data.get("statusCode") or 500,
                message=data.get("message", "Unknown error"),
                error_type=data.get("name", "InternalServerError"),
            )

        return cast(T, data)

    def perform_with_content(self) -> T:
        resp = self.perform()
        if resp is None:
            raise NoContentError()
        return resp

    def __get_headers(self) -> HeadersType:
        headers: HeadersType = {
            "Accept": "application/json",
            "Authorization": f"Bearer {resend.api_key}",
            "User-Agent": f"resend-python:{get_version()}",
        }

        if self.verb == "post" and self.options and "idempotency_key" in self.options:
            headers["Idempotency-Key"] = str(self.options["idempotency_key"])

        if self.verb == "post" and self.options and "batch_validation" in self.options:
            headers["x-batch-validation"] = str(self.options["batch_validation"])

        return headers

    def make_request(self, url: str) -> Union[Dict[str, Any], List[Any]]:
        headers = self.__get_headers()

        if isinstance(self.params, dict):
            json_params: Optional[Union[Dict[str, Any], List[Any]]] = {
                str(k): v for k, v in self.params.items()
            }
        elif isinstance(self.params, list):
            json_params = [dict(item) for item in self.params]
        else:
            json_params = None

        try:
            content, _status_code, resp_headers = resend.default_http_client.request(
                method=self.verb,
                url=url,
                headers=headers,
                json=json_params,
            )

        # Safety net around the HTTP Client
        except Exception as e:
            raise ResendError(
                code=500,
                message=str(e),
                error_type="HttpClientError",
                suggested_action="Request failed, please try again.",
            )

        content_type = {k.lower(): v for k, v in resp_headers.items()}.get(
            "content-type", ""
        )

        if "application/json" not in content_type:
            raise_for_code_and_type(
                code=500,
                message=f"Expected JSON response but got: {content_type}",
                error_type="InternalServerError",
            )

        try:
            return cast(Union[Dict[str, Any], List[Any]], json.loads(content))
        except json.JSONDecodeError:
            raise_for_code_and_type(
                code=500,
                message="Failed to decode JSON response",
                error_type="InternalServerError",
            )
