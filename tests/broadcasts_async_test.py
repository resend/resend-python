import pytest

import resend
from resend.exceptions import NoContentError, ResendError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendBroadcastsAsync(AsyncResendBaseTest):
    async def test_broadcasts_create_async(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"})

        params: resend.Broadcasts.CreateParams = {
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "from": "hi@example.com",
            "subject": "Hello, world!",
            "name": "Python SDK Broadcast",
        }
        broadcast: resend.Broadcasts.CreateResponse = (
            await resend.Broadcasts.create_async(params)
        )
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    async def test_should_create_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Broadcasts.CreateParams = {
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "from": "hi@example.com",
            "subject": "Hello, world!",
            "name": "Python SDK Broadcast",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.create_async(params)

    async def test_broadcasts_update_async(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"})

        params: resend.Broadcasts.UpdateParams = {
            "broadcast_id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "subject": "Hello, world! Updated!",
            "name": "Python SDK Broadcast",
        }
        broadcast: resend.Broadcasts.UpdateResponse = (
            await resend.Broadcasts.update_async(params)
        )
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    async def test_should_update_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Broadcasts.UpdateParams = {
            "broadcast_id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "subject": "Hello, world! Updated!",
            "name": "Python SDK Broadcast",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.update_async(params)

    async def test_broadcasts_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "broadcast",
                "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
                "name": "Announcements",
                "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "from": "Acme <onboarding@resend.dev>",
                "subject": "hello world",
                "reply_to": None,
                "preview_text": "Check out our latest announcements",
                "status": "draft",
                "created_at": "2024-12-01 19:32:22.98+00",
                "scheduled_at": None,
                "sent_at": None,
            }
        )

        broadcast = await resend.Broadcasts.get_async(
            id="559ac32e-9ef5-46fb-82a1-b76b840c0f7b"
        )
        assert broadcast["id"] == "559ac32e-9ef5-46fb-82a1-b76b840c0f7b"
        assert broadcast["name"] == "Announcements"
        assert broadcast["audience_id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert broadcast["from"] == "Acme <onboarding@resend.dev>"
        assert broadcast["subject"] == "hello world"
        assert broadcast["reply_to"] is None
        assert broadcast["preview_text"] == "Check out our latest announcements"
        assert broadcast["status"] == "draft"
        assert broadcast["created_at"] == "2024-12-01 19:32:22.98+00"
        assert broadcast["scheduled_at"] is None
        assert broadcast["sent_at"] is None

    async def test_should_get_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.get_async(
                id="559ac32e-9ef5-46fb-82a1-b76b840c0f7b"
            )

    async def test_broadcasts_send_async(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e791"})

        params: resend.Broadcasts.SendParams = {
            "broadcast_id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
        }
        broadcast = await resend.Broadcasts.send_async(params)
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e791"

    async def test_should_send_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Broadcasts.SendParams = {
            "broadcast_id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.send_async(params)

    async def test_broadcasts_cancel_async(self) -> None:
        self.set_mock_json(
            {
                "object": "broadcast",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        canceled = await resend.Broadcasts.cancel_async(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert canceled["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert canceled["object"] == "broadcast"

    async def test_should_cancel_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.cancel_async(
                "78261eea-8f8b-4381-83c6-79fa7120f1cf"
            )

    async def test_broadcasts_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "broadcasts",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        rmed = await resend.Broadcasts.remove_async(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

    async def test_should_remove_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.remove_async(
                id="78261eea-8f8b-4381-83c6-79fa7120f1cf"
            )

    async def test_broadcasts_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "data": [
                    {
                        "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
                        "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "status": "draft",
                        "created_at": "2024-11-01 15:13:31.723+00",
                        "scheduled_at": None,
                        "sent_at": None,
                    },
                    {
                        "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
                        "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "status": "sent",
                        "created_at": "2024-12-01 19:32:22.98+00",
                        "scheduled_at": "2024-12-02 19:32:22.98+00",
                        "sent_at": "2024-12-02 19:32:22.98+00",
                    },
                ],
            }
        )

        broadcasts: resend.Broadcasts.ListResponse = (
            await resend.Broadcasts.list_async()
        )
        assert broadcasts["object"] == "list"
        assert len(broadcasts["data"]) == 2

        broadcast = broadcasts["data"][0]
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert broadcast["audience_id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert broadcast["status"] == "draft"
        assert broadcast["created_at"] == "2024-11-01 15:13:31.723+00"
        assert broadcast["scheduled_at"] is None
        assert broadcast["sent_at"] is None

        broadcast = broadcasts["data"][1]
        assert broadcast["id"] == "559ac32e-9ef5-46fb-82a1-b76b840c0f7b"
        assert broadcast["audience_id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert broadcast["status"] == "sent"
        assert broadcast["created_at"] == "2024-12-01 19:32:22.98+00"
        assert broadcast["scheduled_at"] == "2024-12-02 19:32:22.98+00"
        assert broadcast["sent_at"] == "2024-12-02 19:32:22.98+00"

    async def test_should_list_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.list_async()

    async def test_broadcasts_recipients_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b2Zmc2V0OjA",
                        "contact_id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "email": "carter@example.com",
                    }
                ],
            }
        )

        params: resend.Broadcasts.RecipientsParams = {
            "broadcast_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            "type": "delivered",
        }
        recipients: resend.Broadcasts.RecipientsResponse = (
            await resend.Broadcasts.recipients_async(params)
        )
        assert recipients["object"] == "list"
        assert recipients["has_more"] is False
        assert len(recipients["data"]) == 1

        recipient = recipients["data"][0]
        assert recipient["id"] == "b2Zmc2V0OjA"
        assert recipient["contact_id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert recipient["email"] == "carter@example.com"

    async def test_broadcasts_recipients_async_opened_has_count(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b2Zmc2V0OjA",
                        "contact_id": None,
                        "email": "carter@example.com",
                        "count": 3,
                    }
                ],
            }
        )

        params: resend.Broadcasts.RecipientsParams = {
            "broadcast_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            "type": "opened",
        }
        recipients = await resend.Broadcasts.recipients_async(params)
        recipient = recipients["data"][0]
        assert recipient["contact_id"] is None
        assert recipient["count"] == 3

    async def test_broadcasts_recipients_async_clicked_has_clicked_links(
        self,
    ) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b2Zmc2V0OjA",
                        "contact_id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "email": "carter@example.com",
                        "count": 2,
                        "clicked_links": [
                            {"url": "https://resend.com/pricing", "clicks": 2}
                        ],
                    }
                ],
            }
        )

        params: resend.Broadcasts.RecipientsParams = {
            "broadcast_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            "type": "clicked",
            "email": "carter",
            "limit": 10,
        }
        recipients = await resend.Broadcasts.recipients_async(params)
        recipient = recipients["data"][0]
        assert recipient["count"] == 2
        assert recipient["clicked_links"] == [
            {"url": "https://resend.com/pricing", "clicks": 2}
        ]

    async def test_broadcasts_recipients_async_bounced_has_bounce_type(
        self,
    ) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b2Zmc2V0OjA",
                        "contact_id": None,
                        "email": "carter@example.com",
                        "bounce_type": "permanent",
                    }
                ],
            }
        )

        params: resend.Broadcasts.RecipientsParams = {
            "broadcast_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            "type": "bounced",
            "bounce_type": "permanent",
        }
        recipients = await resend.Broadcasts.recipients_async(params)
        recipient = recipients["data"][0]
        assert recipient["bounce_type"] == "permanent"

    async def test_broadcasts_recipients_async_raise_exception_when_not_found(
        self,
    ) -> None:
        self.set_mock_json(
            {
                "statusCode": 404,
                "name": "not_found",
                "message": "Broadcast not found",
            }
        )

        params: resend.Broadcasts.RecipientsParams = {
            "broadcast_id": "does-not-exist",
            "type": "sent",
        }
        with pytest.raises(ResendError):
            _ = await resend.Broadcasts.recipients_async(params)

    async def test_should_recipients_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Broadcasts.RecipientsParams = {
            "broadcast_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            "type": "sent",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.recipients_async(params)

    async def test_broadcasts_clicked_links_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b2Zmc2V0OjA",
                        "url": "https://resend.com/pricing",
                        "clicks": 42,
                        "unique_clicks": 30,
                    },
                    {
                        "id": "b2Zmc2V0OjE",
                        "url": "https://resend.com/docs",
                        "clicks": 17,
                        "unique_clicks": 15,
                    },
                ],
            }
        )

        clicked_links: resend.Broadcasts.ListClickedLinksResponse = (
            await resend.Broadcasts.clicked_links_async(
                "559ac32e-9ef5-46fb-82a1-b76b840c0f7b"
            )
        )
        assert clicked_links["object"] == "list"
        assert clicked_links["has_more"] is False
        assert len(clicked_links["data"]) == 2

        link = clicked_links["data"][0]
        assert link["id"] == "b2Zmc2V0OjA"
        assert link["url"] == "https://resend.com/pricing"
        assert link["clicks"] == 42
        assert link["unique_clicks"] == 30

        link = clicked_links["data"][1]
        assert link["id"] == "b2Zmc2V0OjE"
        assert link["url"] == "https://resend.com/docs"
        assert link["clicks"] == 17
        assert link["unique_clicks"] == 15

    async def test_should_clicked_links_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Broadcasts.clicked_links_async(
                "559ac32e-9ef5-46fb-82a1-b76b840c0f7b"
            )
