import unittest
from unittest.mock import Mock

import resend
from resend.response import ResponseDict


class TestResponseHeadersIntegration(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test environment."""
        resend.api_key = "re_test_key"

    def test_email_send_response_includes_headers(self) -> None:
        """Test that email send response includes headers."""
        # Mock the HTTP client to return headers
        mock_client = Mock()
        mock_client.request.return_value = (
            b'{"id": "email_123", "from": "test@example.com"}',
            200,
            {
                "content-type": "application/json",
                "x-request-id": "req_abc123",
                "x-ratelimit-limit": "100",
                "x-ratelimit-remaining": "95",
                "x-ratelimit-reset": "1699564800",
            },
        )

        # Replace default HTTP client with mock
        original_client = resend.default_http_client
        resend.default_http_client = mock_client

        try:
            # Send email
            response = resend.Emails.send(
                {
                    "from": "test@example.com",
                    "to": "user@example.com",
                    "subject": "Test",
                    "html": "<p>Test</p>",
                }
            )

            # Verify response is a ResponseDict
            assert isinstance(response, ResponseDict)
            assert isinstance(response, dict)

            # Verify backward compatibility - dict access still works
            assert response["id"] == "email_123"
            assert response.get("from") == "test@example.com"

            # Verify new feature - headers are accessible
            assert hasattr(response, "headers")
            assert response.headers["x-request-id"] == "req_abc123"
            assert response.headers["x-ratelimit-limit"] == "100"
            assert response.headers["x-ratelimit-remaining"] == "95"
            assert response.headers["x-ratelimit-reset"] == "1699564800"

        finally:
            # Restore original HTTP client
            resend.default_http_client = original_client

    def test_list_response_headers(self) -> None:
        """Test that list responses work (without ResponseDict wrapping)."""
        # Mock the HTTP client to return a list
        mock_client = Mock()
        mock_client.request.return_value = (
            b'{"data": [{"id": "1"}, {"id": "2"}]}',
            200,
            {
                "content-type": "application/json",
                "x-request-id": "req_xyz",
            },
        )

        original_client = resend.default_http_client
        resend.default_http_client = mock_client

        try:
            # Get API keys list
            response = resend.ApiKeys.list()

            # List responses are ResponseDict with data field
            assert isinstance(response, ResponseDict)
            assert "data" in response
            assert response.headers["x-request-id"] == "req_xyz"

        finally:
            resend.default_http_client = original_client
