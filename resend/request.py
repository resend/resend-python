from typing import Any, Dict, Literal

import requests

import resend
from resend.exceptions import raise_for_code_and_type
from resend.version import get_version

RequestVerb = Literal["get", "post", "put", "patch", "delete"]


# This class wraps the HTTP request creation logic
class Request:
    def __init__(self, path: str, params: Dict[Any, Any], verb: RequestVerb):
        self.path = path
        self.params = params
        self.verb = verb

    def perform(self) -> Any:
        """Is the main function that makes the HTTP request
        to the Resend API. It uses the path, params, and verb attributes
        to make the request.

        Returns:
            Dict: The JSON response from the API

        Raises:
            requests.HTTPError: If the request fails
        """
        resp = self.make_request(url=f"{resend.api_url}{self.path}")

        # delete calls do not return a body
        if resp.text == "" and resp.status_code == 200:
            return None

        # handle error in case there is a statusCode attr present
        # and status != 200
        if resp.status_code != 200 and resp.json().get("statusCode"):
            error = resp.json()
            raise_for_code_and_type(
                code=error.get("statusCode"),
                message=error.get("message"),
                error_type=error.get("name"),
            )
        return resp.json()

    def __get_headers(self) -> Dict[Any, Any]:
        """get_headers returns the HTTP headers that will be
        used for every req.

        Returns:
            Dict: configured HTTP Headers
        """
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {resend.api_key}",
            "User-Agent": f"resend-python:{get_version()}",
        }

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
