from typing import Dict, List

import requests

from resend.exceptions import raise_for_code_and_type

from .version import get_version


class Resend:
    """Resend SDK main client class

    Raises:
        ValueError: raises ValueError when api key is
    """

    base_url: str = "https://api.resend.com"
    timeout_ms: int = 60_000

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Resend API Key is required.")
        self.__api_key = api_key

    def __get_headers(self) -> Dict:
        """get_headers returns the HTTP headers that will be
        used for every req.

        Returns:
            Dict: _description_
        """
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.__api_key}",
            "User-Agent": f"python:{get_version()}",
        }

    def _make_request(self, url, params, headers):
        try:
            return requests.post(url, json=params, headers=headers)
        except requests.HTTPError as e:
            raise e

    def send_email(
        self,
        sender: str,
        to: str,
        subject: str,
        text: str = None,
        bcc: str = None,
        cc: str = None,
        html: str = None,
        attachments: List[Dict] = None,
    ):
        if not sender:
            raise ValueError("sender is required.")
        if not to:
            raise ValueError("to is required.")
        if not subject:
            raise ValueError("subject is required.")

        url = f"{self.base_url}/email"
        headers = self.__get_headers()

        params: Dict = {"to": to, "from": sender, "subject": subject}
        if text:
            params["text"] = text
        elif html:
            params["html"] = html

        if cc:
            params["cc"] = cc
        if bcc:
            params["bcc"] = bcc
        if attachments:
            params["attachments"] = attachments

        resp = self._make_request(url, params, headers)

        if resp.status_code != 200:
            error = resp.json()
            raise_for_code_and_type(
                code=error.get("statusCode"),
                message=error.get("message"),
                error_type=error.get("name"),
            )

        return resp.json()
