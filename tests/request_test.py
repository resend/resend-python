import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

from resend import request
from resend.version import get_version


class TestResendRequest(unittest.TestCase):
    @patch("resend.request.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_request_idempotency_key_is_set(self, mock_requests: MagicMock) -> None:
        mock_response = Mock()
        mock_response.text = "{}"
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {}

        mock_requests.return_value = mock_response

        req = request.Request[Dict[str, Any]](
            path="/test",
            params={},
            verb="post",
            options={"idempotency_key": "abc-123"},
        )

        req.perform()

        self.assertTrue(mock_requests.called, "Expected requests.request to be called")

        _, kwargs = mock_requests.call_args
        headers = kwargs["headers"]

        self.assertEqual(headers["Accept"], "application/json")
        self.assertEqual(headers["Authorization"], "Bearer test_key")
        self.assertEqual(headers["User-Agent"], f"resend-python:{get_version()}")
        self.assertEqual(headers["Idempotency-Key"], "abc-123")

    @patch("resend.request.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_request_idempotency_key_is_not_set(self, mock_requests: MagicMock) -> None:
        mock_response = Mock()
        mock_response.text = "{}"
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {}

        mock_requests.return_value = mock_response

        req = request.Request[Dict[str, Any]](
            path="/test",
            params={},
            verb="post",
        )

        req.perform()

        self.assertTrue(mock_requests.called, "Expected requests.request to be called")

        _, kwargs = mock_requests.call_args
        headers = kwargs["headers"]

        self.assertEqual(headers["Accept"], "application/json")
        self.assertEqual(headers["Authorization"], "Bearer test_key")
        self.assertEqual(headers["User-Agent"], f"resend-python:{get_version()}")
        self.assertNotIn(
            "Idempotency-Key", headers, "Idempotency-Key should not be set"
        )
