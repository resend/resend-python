import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendEventsAsync(AsyncResendBaseTest):
    async def test_events_create_async(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        params: resend.Events.CreateParams = {
            "name": "user.signed_up",
        }
        event = await resend.Events.create_async(params)
        assert event["object"] == "event"
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"

    async def test_events_create_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Events.CreateParams = {"name": "user.signed_up"}
        with pytest.raises(NoContentError):
            _ = await resend.Events.create_async(params)

    async def test_events_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "user.signed_up",
                "schema": {"plan": "string"},
                "created_at": "2024-01-01T00:00:00.000Z",
                "updated_at": None,
            }
        )

        event = await resend.Events.get_async("user.signed_up")
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert event["name"] == "user.signed_up"

    async def test_events_get_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Events.get_async("user.signed_up")

    async def test_events_update_async(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        params: resend.Events.UpdateParams = {
            "identifier": "user.signed_up",
            "schema": {"plan": "string"},
        }
        event = await resend.Events.update_async(params)
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"

    async def test_events_update_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Events.UpdateParams = {
            "identifier": "user.signed_up",
            "schema": None,
        }
        with pytest.raises(NoContentError):
            _ = await resend.Events.update_async(params)

    async def test_events_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        resp = await resend.Events.remove_async("user.signed_up")
        assert resp["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert resp["deleted"] is True

    async def test_events_remove_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Events.remove_async("user.signed_up")

    async def test_events_send_async_with_contact_id(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "event": "user.signed_up",
            }
        )

        params: resend.Events.SendParams = {
            "event": "user.signed_up",
            "contact_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
        }
        resp = await resend.Events.send_async(params)
        assert resp["object"] == "event"
        assert resp["event"] == "user.signed_up"

    async def test_events_send_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Events.SendParams = {
            "event": "user.signed_up",
            "email": "user@example.com",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Events.send_async(params)

    async def test_events_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "name": "user.signed_up",
                        "schema": None,
                        "created_at": "2024-01-01T00:00:00.000Z",
                        "updated_at": None,
                    },
                ],
            }
        )

        events = await resend.Events.list_async()
        assert events["object"] == "list"
        assert events["has_more"] is False
        assert len(events["data"]) == 1
        assert events["data"][0]["name"] == "user.signed_up"

    async def test_events_list_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Events.list_async()
