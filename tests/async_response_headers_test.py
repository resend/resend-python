from unittest.mock import AsyncMock

import pytest

import resend

pytestmark = pytest.mark.asyncio


class TestResponseHeadersIntegrationAsync:
    def setup_method(self) -> None:
        resend.api_key = "re_test_key"

    async def test_email_send_async_response_includes_http_headers(self) -> None:
        """Test that async email send response includes http_headers."""
        mock_client = AsyncMock()
        mock_client.request.return_value = (
            b'{"id": "email_123"}',
            200,
            {
                "content-type": "application/json",
                "x-request-id": "req_abc123",
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "95",
                "x-ratelimit-reset": "1699564800",
            },
        )

        original_client = resend.default_async_http_client
        resend.default_async_http_client = mock_client

        try:
            response = await resend.Emails.send_async(
                {
                    "from": "test@example.com",
                    "to": "user@example.com",
                    "subject": "Test",
                    "html": "<p>Test</p>",
                }
            )

            assert isinstance(response, dict)
            assert response["id"] == "email_123"
            assert "http_headers" in response
            assert response["http_headers"]["x-request-id"] == "req_abc123"
            assert response["http_headers"]["x-ratelimit-limit"] == "100"
            assert response["http_headers"]["x-ratelimit-remaining"] == "95"
            assert response["http_headers"]["x-ratelimit-reset"] == "1699564800"

        finally:
            resend.default_async_http_client = original_client

    async def test_list_async_response_includes_http_headers(self) -> None:
        """Test that async list responses include http_headers."""
        mock_client = AsyncMock()
        mock_client.request.return_value = (
            b'{"data": [{"id": "key_1"}, {"id": "key_2"}]}',
            200,
            {
                "content-type": "application/json",
                "x-request-id": "req_xyz",
            },
        )

        original_client = resend.default_async_http_client
        resend.default_async_http_client = mock_client

        try:
            response = await resend.ApiKeys.list_async()

            assert isinstance(response, dict)
            assert "data" in response
            assert "http_headers" in response
            assert response["http_headers"]["x-request-id"] == "req_xyz"

        finally:
            resend.default_async_http_client = original_client

    async def test_received_email_async_headers_not_overwritten_by_http_headers(
        self,
    ) -> None:
        """
        Regression test: ReceivedEmail.headers (MIME email headers) must not be
        overwritten by the injected http_headers (API response headers).
        """
        mock_client = AsyncMock()
        mock_client.request.return_value = (
            b'{"id": "email_456", "object": "received_email", '
            b'"from": "sender@example.com", "to": ["recipient@example.com"], '
            b'"subject": "Hello", "created_at": "2024-01-01T00:00:00Z", '
            b'"message_id": "msg_123", "attachments": [], '
            b'"headers": {"List-Unsubscribe": "<mailto:unsub@example.com>", '
            b'"X-Custom": "value"}}',
            200,
            {
                "content-type": "application/json",
                "x-request-id": "req_recv_123",
                "x-ratelimit-limit": "100",
            },
        )

        original_client = resend.default_async_http_client
        resend.default_async_http_client = mock_client

        try:
            response = await resend.Emails.Receiving.get_async(email_id="email_456")

            assert isinstance(response, dict)
            assert response["id"] == "email_456"

            # MIME email headers must be intact
            assert "headers" in response
            assert (
                response["headers"]["List-Unsubscribe"] == "<mailto:unsub@example.com>"
            )
            assert response["headers"]["X-Custom"] == "value"

            # HTTP response headers must be injected separately under http_headers
            assert "http_headers" in response
            assert response["http_headers"]["x-request-id"] == "req_recv_123"
            assert response["http_headers"]["x-ratelimit-limit"] == "100"

            # The two must not collide
            assert response["headers"] is not response["http_headers"]

        finally:
            resend.default_async_http_client = original_client

    async def test_send_async_with_custom_email_headers_does_not_collide(
        self,
    ) -> None:
        """
        Test that SendParams.headers (custom email headers sent to the recipient)
        do not collide with http_headers in the response.
        """
        mock_client = AsyncMock()
        mock_client.request.return_value = (
            b'{"id": "email_789"}',
            200,
            {
                "content-type": "application/json",
                "x-request-id": "req_789",
            },
        )

        original_client = resend.default_async_http_client
        resend.default_async_http_client = mock_client

        try:
            response = await resend.Emails.send_async(
                {
                    "from": "test@example.com",
                    "to": "user@example.com",
                    "subject": "Test",
                    "html": "<p>Test</p>",
                    "headers": {"List-Unsubscribe": "<mailto:unsub@example.com>"},
                }
            )

            assert isinstance(response, dict)
            assert response["id"] == "email_789"
            # SendResponse does not echo back SendParams.headers — only id is returned
            assert "headers" not in response
            assert "http_headers" in response
            assert response["http_headers"]["x-request-id"] == "req_789"

        finally:
            resend.default_async_http_client = original_client
