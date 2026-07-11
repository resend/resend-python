import unittest
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from resend import request
from resend.exceptions import ApplicationError, ResendError
from resend.version import get_version


class TestResendRequest(unittest.TestCase):
    @patch("resend.http_client_requests.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_request_idempotency_key_is_set(self, mock_requests: MagicMock) -> None:
        mock_response = Mock()
        mock_response.content = b"{}"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
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

    @patch("resend.http_client_requests.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_request_idempotency_key_is_not_set(self, mock_requests: MagicMock) -> None:
        mock_response = Mock()
        mock_response.content = b"{}"
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

    @patch("resend.http_client_requests.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_non_json_preserves_http_status_when_client_error(
        self, mock_requests: MagicMock
    ) -> None:
        mock_response = Mock()
        mock_response.content = b"<html>rate limited</html>"
        mock_response.status_code = 429
        mock_response.headers = {
            "Content-Type": "text/html",
            "retry-after": "2",
        }
        mock_requests.return_value = mock_response

        req = request.Request[Dict[str, Any]](
            path="/emails",
            params={},
            verb="post",
        )

        with self.assertRaises(ResendError) as ctx:
            req.perform()

        err = ctx.exception
        self.assertEqual(err.code, 429)
        self.assertEqual(err.error_type, "application_error")
        self.assertIn("text/html", err.message)
        self.assertEqual(err.headers.get("retry-after"), "2")

    @patch("resend.http_client_requests.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_non_json_preserves_http_status_when_server_error(
        self, mock_requests: MagicMock
    ) -> None:
        mock_response = Mock()
        mock_response.content = b""
        mock_response.status_code = 503
        mock_response.headers = {"content-type": "text/plain"}
        mock_requests.return_value = mock_response

        req = request.Request[Dict[str, Any]](
            path="/emails",
            params={},
            verb="get",
        )

        with self.assertRaises(ResendError) as ctx:
            req.perform()

        err = ctx.exception
        self.assertEqual(err.code, 503)
        self.assertEqual(err.error_type, "application_error")

    @patch("resend.http_client_requests.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_non_json_falls_back_to_500_when_status_is_success(
        self, mock_requests: MagicMock
    ) -> None:
        mock_response = Mock()
        mock_response.content = b"<html>ok?</html>"
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "text/html; charset=utf-8"}
        mock_requests.return_value = mock_response

        req = request.Request[Dict[str, Any]](
            path="/emails",
            params={},
            verb="post",
        )

        with self.assertRaises(ApplicationError) as ctx:
            req.perform()

        err = ctx.exception
        self.assertEqual(err.code, 500)
        self.assertEqual(err.error_type, "application_error")
        self.assertIn("text/html", err.message)

    @patch("resend.http_client_requests.requests.request")
    @patch("resend.api_key", new="test_key")
    def test_invalid_json_preserves_http_status(self, mock_requests: MagicMock) -> None:
        mock_response = Mock()
        mock_response.content = b"not-json"
        mock_response.status_code = 502
        mock_response.headers = {"content-type": "application/json"}
        mock_requests.return_value = mock_response

        req = request.Request[Dict[str, Any]](
            path="/emails",
            params={},
            verb="get",
        )

        with self.assertRaises(ResendError) as ctx:
            req.perform()

        err = ctx.exception
        self.assertEqual(err.code, 502)
        self.assertEqual(err.error_type, "application_error")
        self.assertEqual(err.message, "Failed to decode JSON response")


@pytest.mark.asyncio
class TestResendAsyncRequestNonJson:
    async def test_async_non_json_preserves_http_status(self) -> None:

        import resend
        from resend import async_request

        mock_client = AsyncMock()
        mock_client.request.return_value = (
            b"<html>unauthorized</html>",
            401,
            {"content-type": "text/html"},
        )

        original = resend.default_async_http_client
        resend.api_key = "test_key"
        resend.default_async_http_client = mock_client
        try:
            req = async_request.AsyncRequest[Dict[str, Any]](
                path="/emails",
                params={},
                verb="get",
            )
            with pytest.raises(ResendError) as ctx:
                await req.perform()

            err = ctx.value
            assert err.code == 401
            assert err.error_type == "application_error"
            assert "text/html" in err.message
        finally:
            resend.default_async_http_client = original
