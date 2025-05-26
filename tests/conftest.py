from typing import Any
from unittest import TestCase
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class ResendBaseTest(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_123"
        resend.default_http_client = resend.RequestsClient()
        self.patcher = patch("resend.request.Request.make_request")
        self.mock = self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def set_mock_json(self, mock_json: Any) -> None:
        """Auxiliary function to set the mock json return value"""
        self.mock.return_value = mock_json

    def set_mock_text(self, mock_text: str) -> None:
        """Auxiliary function to set the mock text return value"""
        self.mock.text = mock_text

    def set_magic_mock_obj(self, magic_mock_obj: MagicMock) -> None:
        """Auxiliary function to set the mock object"""
        self.mock.return_value = magic_mock_obj
