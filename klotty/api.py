from typing import Dict
from .version import get_version
import requests


class Klotty:
    """Klotty SDK main client class

    Raises:
        ValueError: raises ValueError when api key is
    """

    base_url: str = "https://api.klotty.com"
    timeout_ms: int = 60_000

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Klotty API Key is required.")
        self.__api_key = api_key

    def send_email(
        self,
        sender: str,
        to: str,
        subject: str,
        text: str = None,
        bcc: str = None,
        cc: str = None,
        html: str = None,
    ):
        if not sender:
            raise ValueError("sender is required.")
        if not to:
            raise ValueError("to is required.")
        if not subject:
            raise ValueError("subject is required.")

        url = f"{self.base_url}/email"
        headers: Dict[str, str] = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.__api_key}",
            "User-Agent": f"python:{get_version()}",
        }

        params: Dict = {"to": to, "from": sender, "subject": subject}
        if text:
            params["text"] = text

        requests.post(url, json=params, headers=headers)
