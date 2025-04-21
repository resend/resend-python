from typing import Any, Dict, Generic, List, Optional, Union, cast

import requests
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
        """Is the main function that makes the HTTP request
        to the Resend API. It uses the path, params, and verb attributes
        to make the request.

        Returns:
            Union[T, None]: A generic type of the Request class or None

        Raises:
            requests.HTTPError: If the request fails
        """
        resp = self.make_request(url=f"{resend.api_url}{self.path}")

        # delete calls do not return a body
        if resp.text == "" and resp.status_code == 200:
            return None

        # this is a safety net, if we get here it means the Resend API is having issues
        # and most likely the gateway is returning htmls
        if "application/json" not in resp.headers["content-type"]:
            raise_for_code_and_type(
                code=500,
                message="Failed to parse Resend API response. Please try again.",
                error_type="InternalServerError",
            )

        # handle error in case there is a statusCode attr present
        # and status != 200 and response is a json.
        if resp.status_code != 200 and resp.json().get("statusCode"):
            error = resp.json()
            raise_for_code_and_type(
                code=error.get("statusCode"),
                message=error.get("message"),
                error_type=error.get("name"),
            )
        return cast(T, resp.json())

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

    def make_request(self, url: str) -> requests.Response:
        """make_request is a helper function that makes the actual
        HTTP request to the Resend API.

        Args:
            url (str): The URL to make the request to

        Returns:
            requests.Response: The response object from the request

        Raises:
            requests.HTTPError: If the request fails
        """
        headers = self.__get_headers()
        params = self.params
        verb = self.verb

        try:
            return requests.request(verb, url, json=params, headers=headers)
        except requests.HTTPError as e:
            raise e
