import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendWebhooksAsync(AsyncResendBaseTest):
    async def test_webhooks_create_async(self) -> None:
        self.set_mock_json(
            {
                "object": "webhook",
                "id": "wh_123",
                "signing_secret": "whsec_test123",
            }
        )

        params: resend.Webhooks.CreateParams = {
            "endpoint": "https://example.com/webhook",
            "events": ["email.sent", "email.delivered"],
        }
        webhook = await resend.Webhooks.create_async(params)
        assert webhook["id"] == "wh_123"
        assert webhook["signing_secret"] == "whsec_test123"

    async def test_should_create_webhooks_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Webhooks.CreateParams = {
            "endpoint": "https://example.com/webhook",
            "events": ["email.sent"],
        }
        with pytest.raises(NoContentError):
            _ = await resend.Webhooks.create_async(params)

    async def test_webhooks_get_async(self) -> None:
        self.set_mock_json(
            {
                "id": "wh_123",
                "object": "webhook",
                "created_at": "2024-01-01T00:00:00Z",
                "status": "enabled",
                "endpoint": "https://example.com/webhook",
                "events": ["email.sent"],
                "signing_secret": None,
            }
        )

        webhook = await resend.Webhooks.get_async("wh_123")
        assert webhook["id"] == "wh_123"
        assert webhook["endpoint"] == "https://example.com/webhook"
        assert webhook["status"] == "enabled"

    async def test_should_get_webhooks_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Webhooks.get_async("wh_123")

    async def test_webhooks_update_async(self) -> None:
        self.set_mock_json({"object": "webhook", "id": "wh_123"})

        params: resend.Webhooks.UpdateParams = {
            "webhook_id": "wh_123",
            "endpoint": "https://new-endpoint.com/webhook",
            "status": "disabled",
        }
        webhook = await resend.Webhooks.update_async(params)
        assert webhook["id"] == "wh_123"

    async def test_should_update_webhooks_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Webhooks.UpdateParams = {
            "webhook_id": "wh_123",
            "endpoint": "https://new-endpoint.com/webhook",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Webhooks.update_async(params)

    async def test_webhooks_list_async(self) -> None:
        self.set_mock_json(
            {
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
        )

        webhooks = await resend.Webhooks.list_async()
        assert webhooks["object"] == "list"
        assert len(webhooks["data"]) == 1
        assert webhooks["data"][0]["id"] == "wh_123"

    async def test_should_list_webhooks_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Webhooks.list_async()

    async def test_webhooks_remove_async(self) -> None:
        self.set_mock_json({"object": "webhook", "id": "wh_123", "deleted": True})

        result = await resend.Webhooks.remove_async("wh_123")
        assert result["id"] == "wh_123"
        assert result["deleted"] is True

    async def test_should_remove_webhooks_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Webhooks.remove_async("wh_123")
