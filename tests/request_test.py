import unittest
from typing import Any, Dict
from resend.request import Request
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class TestRequest(unittest.TestCase):
    def test_request_replace_params(self) -> None:
        params: Dict[Any, Any] = {
            "to": "to@to.com",
            "sender": "sender",
            "subject": "hey",
        }
        params2: Dict[Any, Any] = {
            "to": "to@to.com",
            "from_": "from_",
            "subject": "hey",
        }
        assert Request(
            path="/path", params=params, verb="post"
        ).params == {
            "to": "to@to.com",
            "from": "sender",
            "subject": "hey",
        }
        assert Request(
            path="/path", params=params2, verb="post"
        ).params == {
            "to": "to@to.com",
            "from": "from_",
            "subject": "hey",
        }