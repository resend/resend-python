import base64
import hmac
import time
from hashlib import sha256
from typing import Any, Dict

import pytest

import resend
from tests.conftest import ResendBaseTest


class TestWebhooks(ResendBaseTest):
    def test_webhooks_create(self) -> None:
        create_webhook_response = {
            "object": "webhook",
            "id": "wh_123",
            "signing_secret": "whsec_test123",
        }
        self.set_mock_json(create_webhook_response)

        params: resend.Webhooks.CreateParams = {
            "endpoint": "https://example.com/webhook",
            "events": ["email.sent", "email.delivered"],
        }

        webhook = resend.Webhooks.create(params)
        assert webhook["id"] == "wh_123"
        assert webhook["signing_secret"] == "whsec_test123"

    def test_webhooks_get(self) -> None:
        webhook_response = {
            "id": "wh_123",
            "object": "webhook",
            "created_at": "2024-01-01T00:00:00Z",
            "status": "enabled",
            "endpoint": "https://example.com/webhook",
            "events": ["email.sent"],
            "signing_secret": None,
        }
        self.set_mock_json(webhook_response)

        webhook = resend.Webhooks.get("wh_123")
        assert webhook["id"] == "wh_123"
        assert webhook["endpoint"] == "https://example.com/webhook"
        assert webhook["status"] == "enabled"

    def test_webhooks_update(self) -> None:
        update_response = {"object": "webhook", "id": "wh_123"}
        self.set_mock_json(update_response)

        params: resend.Webhooks.UpdateParams = {
            "webhook_id": "wh_123",
            "endpoint": "https://new-endpoint.com/webhook",
            "status": "disabled",
        }

        webhook = resend.Webhooks.update(params)
        assert webhook["id"] == "wh_123"

    def test_webhooks_list(self) -> None:
        list_response = {
            "object": "list",
            "data": [
                {
                    "id": "wh_123",
                    "object": "webhook",
                    "created_at": "2024-01-01T00:00:00Z",
                    "status": "enabled",
                    "endpoint": "https://example.com/webhook",
                    "events": ["email.sent"],
                    "signing_secret": None,
                }
            ],
            "has_more": False,
        }
        self.set_mock_json(list_response)

        webhooks = resend.Webhooks.list()
        assert webhooks["object"] == "list"
        assert len(webhooks["data"]) == 1
        assert webhooks["data"][0]["id"] == "wh_123"

    def test_webhooks_remove(self) -> None:
        delete_response = {"object": "webhook", "id": "wh_123", "deleted": True}
        self.set_mock_json(delete_response)

        result = resend.Webhooks.remove("wh_123")
        assert result["id"] == "wh_123"
        assert result["deleted"] is True


class TestWebhookVerification:
    """Test webhook signature verification"""

    def _generate_test_signature(
        self, secret: str, msg_id: str, timestamp: str, payload: str
    ) -> str:
        """Generate a valid signature for testing"""
        # Remove whsec_ prefix and decode
        secret_bytes = base64.b64decode(secret.replace("whsec_", ""))

        # Construct signed content
        signed_content = f"{msg_id}.{timestamp}.{payload}"

        # Generate signature
        h = hmac.new(secret_bytes, signed_content.encode("utf-8"), sha256)
        signature = base64.b64encode(h.digest()).decode("utf-8")

        return f"v1,{signature}"

    def test_verify_valid_webhook(self) -> None:
        """Test successful webhook verification"""
        # Use a base64-encoded secret
        secret = "whsec_" + base64.b64encode(b"test_secret_key").decode("utf-8")
        msg_id = "msg_123"
        timestamp = str(int(time.time()))
        payload = '{"type":"email.sent","data":{"email_id":"123"}}'

        signature = self._generate_test_signature(secret, msg_id, timestamp, payload)

        headers: resend.WebhookHeaders = {
            "id": msg_id,
            "timestamp": timestamp,
            "signature": signature,
        }

        options: resend.VerifyWebhookOptions = {
            "payload": payload,
            "headers": headers,
            "webhook_secret": secret,
        }

        # Should not raise an exception
        resend.Webhooks.verify(options)

    def test_verify_invalid_signature(self) -> None:
        """Test webhook verification with invalid signature"""
        secret = "whsec_" + base64.b64encode(b"test_secret_key").decode("utf-8")
        msg_id = "msg_123"
        timestamp = str(int(time.time()))
        payload = '{"type":"email.sent","data":{"email_id":"123"}}'

        headers: resend.WebhookHeaders = {
            "id": msg_id,
            "timestamp": timestamp,
            "signature": "v1,invalid_signature",
        }

        options: resend.VerifyWebhookOptions = {
            "payload": payload,
            "headers": headers,
            "webhook_secret": secret,
        }

        with pytest.raises(ValueError, match="no matching signature found"):
            resend.Webhooks.verify(options)

    def test_verify_expired_timestamp(self) -> None:
        """Test webhook verification with expired timestamp"""
        secret = "whsec_" + base64.b64encode(b"test_secret_key").decode("utf-8")
        msg_id = "msg_123"
        # Timestamp from 10 minutes ago (beyond the 5-minute tolerance)
        timestamp = str(int(time.time()) - 600)
        payload = '{"type":"email.sent","data":{"email_id":"123"}}'

        signature = self._generate_test_signature(secret, msg_id, timestamp, payload)

        headers: resend.WebhookHeaders = {
            "id": msg_id,
            "timestamp": timestamp,
            "signature": signature,
        }

        options: resend.VerifyWebhookOptions = {
            "payload": payload,
            "headers": headers,
            "webhook_secret": secret,
        }

        with pytest.raises(ValueError, match="timestamp outside tolerance window"):
            resend.Webhooks.verify(options)

    def test_verify_missing_payload(self) -> None:
        """Test webhook verification with missing payload"""
        secret = "whsec_test123"

        headers: resend.WebhookHeaders = {
            "id": "msg_123",
            "timestamp": str(int(time.time())),
            "signature": "v1,sig",
        }

        options: Dict[str, Any] = {
            "payload": "",
            "headers": headers,
            "webhook_secret": secret,
        }

        with pytest.raises(ValueError, match="payload cannot be empty"):
            resend.Webhooks.verify(options)  # type: ignore

    def test_verify_missing_webhook_secret(self) -> None:
        """Test webhook verification with missing webhook secret"""
        headers: resend.WebhookHeaders = {
            "id": "msg_123",
            "timestamp": str(int(time.time())),
            "signature": "v1,sig",
        }

        options: Dict[str, Any] = {
            "payload": "test",
            "headers": headers,
            "webhook_secret": "",
        }

        with pytest.raises(ValueError, match="webhook_secret cannot be empty"):
            resend.Webhooks.verify(options)  # type: ignore

    def test_verify_missing_headers(self) -> None:
        """Test webhook verification with missing headers"""
        secret = "whsec_test123"

        # Test missing svix-id
        headers: resend.WebhookHeaders = {
            "id": "",
            "timestamp": str(int(time.time())),
            "signature": "v1,sig",
        }

        options: resend.VerifyWebhookOptions = {
            "payload": "test",
            "headers": headers,
            "webhook_secret": secret,
        }

        with pytest.raises(ValueError, match="svix-id header is required"):
            resend.Webhooks.verify(options)

    def test_verify_invalid_timestamp_format(self) -> None:
        """Test webhook verification with invalid timestamp format"""
        secret = "whsec_" + base64.b64encode(b"test_secret_key").decode("utf-8")

        headers: resend.WebhookHeaders = {
            "id": "msg_123",
            "timestamp": "not_a_number",
            "signature": "v1,sig",
        }

        options: resend.VerifyWebhookOptions = {
            "payload": "test",
            "headers": headers,
            "webhook_secret": secret,
        }

        with pytest.raises(ValueError, match="invalid timestamp format"):
            resend.Webhooks.verify(options)

    def test_verify_multiple_signatures(self) -> None:
        """Test webhook verification with multiple signatures (one valid)"""
        secret = "whsec_" + base64.b64encode(b"test_secret_key").decode("utf-8")
        msg_id = "msg_123"
        timestamp = str(int(time.time()))
        payload = '{"type":"email.sent","data":{"email_id":"123"}}'

        valid_signature = self._generate_test_signature(
            secret, msg_id, timestamp, payload
        )

        # Create signature header with multiple signatures (Svix format)
        headers: resend.WebhookHeaders = {
            "id": msg_id,
            "timestamp": timestamp,
            "signature": f"v1,invalid_sig1 {valid_signature} v1,invalid_sig2",
        }

        options: resend.VerifyWebhookOptions = {
            "payload": payload,
            "headers": headers,
            "webhook_secret": secret,
        }

        # Should not raise an exception (finds the valid signature)
        resend.Webhooks.verify(options)

    def test_verify_tampered_payload(self) -> None:
        """Test webhook verification with tampered payload"""
        secret = "whsec_" + base64.b64encode(b"test_secret_key").decode("utf-8")
        msg_id = "msg_123"
        timestamp = str(int(time.time()))
        original_payload = '{"type":"email.sent","data":{"email_id":"123"}}'

        # Generate signature with original payload
        signature = self._generate_test_signature(
            secret, msg_id, timestamp, original_payload
        )

        # But try to verify with tampered payload
        tampered_payload = '{"type":"email.sent","data":{"email_id":"456"}}'

        headers: resend.WebhookHeaders = {
            "id": msg_id,
            "timestamp": timestamp,
            "signature": signature,
        }

        options: resend.VerifyWebhookOptions = {
            "payload": tampered_payload,
            "headers": headers,
            "webhook_secret": secret,
        }

        with pytest.raises(ValueError, match="no matching signature found"):
            resend.Webhooks.verify(options)
