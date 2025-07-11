from typing import Any, Dict, Mapping, Tuple, cast
from unittest import TestCase
from unittest.mock import create_autospec

import pytest

import resend
import resend.exceptions
from resend.http_client import HTTPClient


class TestDefaultHttpClientUsage(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_test"
        resend.default_http_client = cast(HTTPClient, None)

    def tearDown(self) -> None:
        resend.api_key = None
        resend.default_http_client = cast(HTTPClient, None)

    def test_default_http_client_called_with_correct_payload(self) -> None:
        mock_client = create_autospec(HTTPClient, instance=True)
        mock_client.name = "mock"
        mock_client.request.return_value = (
            b'{"id": "email_123"}',
            200,
            {"Content-Type": "application/json"},
        )

        resend.default_http_client = mock_client

        resend.Emails.send(
            {
                "from": "hello@example.com",
                "to": ["world@example.com"],
                "subject": "Hi!",
                "html": "<b>hi</b>",
            }
        )

        mock_client.request.assert_called_once()
        args, kwargs = mock_client.request.call_args
        assert kwargs["method"] == "post"
        assert "/emails" in kwargs["url"]
        assert kwargs["json"]["subject"] == "Hi!"

    def test_perform_raises_resend_error_on_runtime_error(self) -> None:
        class RaisesClient(resend.http_client.HTTPClient):
            def request(
                self, *args: object, **kwargs: object
            ) -> Tuple[bytes, int, Mapping[str, str]]:
                raise RuntimeError("Connection broken")

        resend.default_http_client = RaisesClient()

        request: resend.Request[Dict[str, Any]] = resend.Request(
            path="/emails", params={}, verb="post"
        )

        with pytest.raises(resend.exceptions.ResendError) as exc:
            request.perform()

        assert "Connection broken" in str(exc.value)
        assert exc.value.error_type == "HttpClientError"
