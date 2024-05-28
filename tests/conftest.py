from typing import Any, Dict
from unittest import TestCase
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class ResendBaseTest(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_123"

        self.patcher = patch("resend.Request.make_request")
        self.mock = self.patcher.start()
        self.mock.status_code = 200
        self.m = MagicMock()
        self.m.status_code = 200
        self.mock.return_value = self.m

    def tearDown(self) -> None:
        self.patcher.stop()

    def set_mock_json(self, mock_json: Dict[Any, Any]) -> None:
        """Auxiliary function to set the mock json return value"""
        self.m.json = lambda: mock_json

    def set_mock_text(self, mock_text: str) -> None:
        """Auxiliary function to set the mock text return value"""
        self.m.text = mock_text
