import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendBroadcastsAsync(ResendBaseTest):
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
        with self.assertRaises(NoContentError):
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
        with self.assertRaises(NoContentError):
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
                "created_at": "2024-12-01T19:32:22.980Z",
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
        assert broadcast["created_at"] == "2024-12-01T19:32:22.980Z"
        assert broadcast["scheduled_at"] is None
        assert broadcast["sent_at"] is None

    async def test_should_get_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
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
        with self.assertRaises(NoContentError):
            _ = await resend.Broadcasts.send_async(params)

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
        with self.assertRaises(NoContentError):
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
                        "created_at": "2024-11-01T15:13:31.723Z",
                        "scheduled_at": None,
                        "sent_at": None,
                    },
                    {
                        "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
                        "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "status": "sent",
                        "created_at": "2024-12-01T19:32:22.980Z",
                        "scheduled_at": "2024-12-02T19:32:22.980Z",
                        "sent_at": "2024-12-02T19:32:22.980Z",
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
        assert broadcast["created_at"] == "2024-11-01T15:13:31.723Z"
        assert broadcast["scheduled_at"] is None
        assert broadcast["sent_at"] is None

        broadcast = broadcasts["data"][1]
        assert broadcast["id"] == "559ac32e-9ef5-46fb-82a1-b76b840c0f7b"
        assert broadcast["audience_id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert broadcast["status"] == "sent"
        assert broadcast["created_at"] == "2024-12-01T19:32:22.980Z"
        assert broadcast["scheduled_at"] == "2024-12-02T19:32:22.980Z"
        assert broadcast["sent_at"] == "2024-12-02T19:32:22.980Z"

    async def test_should_list_broadcasts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.Broadcasts.list_async()
