from unittest.mock import AsyncMock

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
                "created_at": "2024-01-01 00:00:00+00",
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
                        "created_at": "2024-01-01 00:00:00+00",
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

    async def test_webhooks_list_events_async(self) -> None:
        response = {
            "object": "list",
            "has_more": True,
            "data": [
                {
                    "id": "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2",
                    "type": "email.sent",
                    "created_at": "2024-01-01T00:00:00.000Z",
                    "status": "success",
                }
            ],
        }
        self.set_mock_json(response)
        params: resend.Webhooks.ListEventsParams = {
            "limit": 10,
            "after": "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2",
        }

        events = await resend.Webhooks.list_events_async("wh_123", params)

        assert events == response
        self.mock.assert_awaited_once_with(
            url="https://api.resend.com/webhooks/wh_123/events?limit=10&after=msg_1srOrx2ZWZBpBUvZwXKQmoEYga2"
        )

    async def test_webhooks_get_event_async(self) -> None:
        response = {
            "object": "webhook_event",
            "id": "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2",
            "type": "email.sent",
            "created_at": "2024-01-01T00:00:00.000Z",
            "status": "pending",
            "next_attempt_at": None,
            "payload": {
                "type": "email.sent",
                "created_at": "2024-01-01T00:00:00.000Z",
                "data": {},
            },
        }
        self.set_mock_json(response)

        event = await resend.Webhooks.get_event_async(
            "wh_123", "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2"
        )

        assert event == response
        self.mock.assert_awaited_once_with(
            url="https://api.resend.com/webhooks/wh_123/events/msg_1srOrx2ZWZBpBUvZwXKQmoEYga2"
        )

    async def test_should_replay_event_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Webhooks.replay_event_async(
                "wh_123", "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2"
            )

    async def test_webhooks_list_event_attempts_async(self) -> None:
        response = {
            "object": "list",
            "has_more": False,
            "data": [
                {
                    "id": "atmpt_2ZbUCwvGmIT4mLIN6d3Yz0Ainbd",
                    "http_status_code": 200,
                    "response": "OK",
                    "sent_at": "2024-01-01T00:00:00.000Z",
                }
            ],
        }
        self.set_mock_json(response)
        params: resend.Webhooks.ListEventAttemptsParams = {
            "limit": 5,
            "after": "atmpt_2ZbUCwvGmIT4mLIN6d3Yz0Ainbd",
        }

        attempts = await resend.Webhooks.list_event_attempts_async(
            "wh_123", "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2", params
        )

        assert attempts == response
        self.mock.assert_awaited_once_with(
            url="https://api.resend.com/webhooks/wh_123/events/msg_1srOrx2ZWZBpBUvZwXKQmoEYga2/attempts?limit=5&after=atmpt_2ZbUCwvGmIT4mLIN6d3Yz0Ainbd"
        )

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


class TestWebhooksRequestAsync:
    def setup_method(self) -> None:
        resend.api_key = "re_123"
        self.mock_client = AsyncMock()
        self.mock_client.request.return_value = (
            b'{"object": "webhook_event", "id": "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2"}',
            200,
            {"content-type": "application/json"},
        )
        self.previous_async_http_client = resend.default_async_http_client
        resend.default_async_http_client = self.mock_client

    def teardown_method(self) -> None:
        resend.default_async_http_client = self.previous_async_http_client

    async def test_replay_event_async_posts_to_the_replay_path(self) -> None:
        event = await resend.Webhooks.replay_event_async(
            "wh_123", "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2"
        )

        assert event["object"] == "webhook_event"
        assert event["id"] == "msg_1srOrx2ZWZBpBUvZwXKQmoEYga2"
        _, kwargs = self.mock_client.request.call_args
        assert kwargs["method"] == "post"
        assert (
            kwargs["url"]
            == "https://api.resend.com/webhooks/wh_123/events/msg_1srOrx2ZWZBpBUvZwXKQmoEYga2/replay"
        )
