from typing import Dict

import requests

import resend
from resend.exceptions import raise_for_code_and_type
from resend.version import get_version


# This class wraps the HTTP request creation logic
class Request:
    base_url: str = "https://api.resend.com"

    def __init__(self, path: str, params: Dict, verb: str):
        self.path = path
        self.params = params
        self.verb = verb

    def perform(self):
        resp = self.make_request(url=f"{self.base_url}{self.path}")

        if resp.status_code != 200:
            error = resp.json()
            raise_for_code_and_type(
                code=error.get("statusCode"),
                message=error.get("message"),
                error_type=error.get("name"),
            )

        # some delete calls do not return a body
        if resp.text == "":
            return None
        return resp.json()

    def __get_headers(self) -> Dict:
        """get_headers returns the HTTP headers that will be
        used for every req.

        Returns:
            Dict: configured HTTP Headers
        """
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {resend.api_key}",
            "User-Agent": f"python:{get_version()}",
        }

    def make_request(self, url: str):
        headers = self.__get_headers()
        params = self.params
        verb = self.verb
        try:
            return requests.request(verb, url, json=params, headers=headers)
        except requests.HTTPError as e:
            raise e
