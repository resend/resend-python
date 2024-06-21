from typing import Any
from unittest import TestCase
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class ResendBaseTest(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_123"

        self.patcher = patch("resend.Request.make_request")
        self.mock = self.patcher.start()
        self.m = MagicMock(
            status_code=200,
            headers={"content-type": "application/json; charset=utf-8"},
        )
        self.mock.return_value = self.m

    def tearDown(self) -> None:
        self.patcher.stop()

    def set_mock_json(self, mock_json: Any) -> None:
        """Auxiliary function to set the mock json return value"""
        self.m.json = lambda: mock_json

    def set_mock_text(self, mock_text: str) -> None:
        """Auxiliary function to set the mock text return value"""
        self.m.text = mock_text

    def set_magic_mock_obj(self, magic_mock_obj: MagicMock) -> None:
        """Auxiliary function to set the mock object"""
        self.mock.return_value = magic_mock_obj
