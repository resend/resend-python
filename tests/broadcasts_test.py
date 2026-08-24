import resend
from resend.exceptions import NoContentError, ResendError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendBroadcasts(ResendBaseTest):
    def test_broadcasts_create(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"})

        params: resend.Broadcasts.CreateParams = {
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "from": "hi@example.com",
            "subject": "Hello, world!",
            "name": "Python SDK Broadcast",
        }
        broadcast: resend.Broadcasts.CreateResponse = resend.Broadcasts.create(params)
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_broadcasts_update(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"})

        params: resend.Broadcasts.UpdateParams = {
            "broadcast_id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "subject": "Hello, world! Updated!",
            "name": "Python SDK Broadcast",
        }
        broadcast: resend.Broadcasts.UpdateResponse = resend.Broadcasts.update(params)
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_broadcasts_get(self) -> None:
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
                "html": "<p>Hello World</p>",
                "text": "Hello World",
            }
        )

        broadcast = resend.Broadcasts.get(id="559ac32e-9ef5-46fb-82a1-b76b840c0f7b")
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
        assert broadcast["html"] == "<p>Hello World</p>"
        assert broadcast["text"] == "Hello World"

    def test_broadcasts_send(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e791"})

        params: resend.Broadcasts.SendParams = {
            "broadcast_id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
        }
        broadcast = resend.Broadcasts.send(params)
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e791"

    def test_broadcasts_create_and_send(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"})

        params: resend.Broadcasts.CreateParams = {
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "from": "hi@example.com",
            "subject": "Hello, world!",
            "name": "Python SDK Broadcast",
            "send": True,
        }
        broadcast: resend.Broadcasts.CreateResponse = resend.Broadcasts.create(params)
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_broadcasts_create_and_schedule(self) -> None:
        self.set_mock_json({"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"})

        params: resend.Broadcasts.CreateParams = {
            "audience_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
            "from": "hi@example.com",
            "subject": "Hello, world!",
            "name": "Python SDK Broadcast",
            "send": True,
            "scheduled_at": "2024-12-21T19:32:22.980Z",
        }
        broadcast: resend.Broadcasts.CreateResponse = resend.Broadcasts.create(params)
        assert broadcast["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_broadcasts_cancel(self) -> None:
        self.set_mock_json(
            {
                "object": "broadcast",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        canceled = resend.Broadcasts.cancel("78261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert canceled["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert canceled["object"] == "broadcast"

    def test_broadcasts_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "broadcasts",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        rmed = resend.Broadcasts.remove("78261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

    def test_broadcasts_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
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

        broadcasts: resend.Broadcasts.ListResponse = resend.Broadcasts.list()
        assert broadcasts["object"] == "list"
        assert broadcasts["has_more"] is False
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

    def test_broadcasts_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "broadcast-1",
                        "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "status": "draft",
                        "created_at": "2024-11-01 15:13:31.723+00",
                        "scheduled_at": None,
                        "sent_at": None,
                    },
                    {
                        "id": "broadcast-2",
                        "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "status": "sent",
                        "created_at": "2024-12-01 19:32:22.98+00",
                        "scheduled_at": "2024-12-02 19:32:22.98+00",
                        "sent_at": "2024-12-02 19:32:22.98+00",
                    },
                ],
            }
        )

        params: resend.Broadcasts.ListParams = {
            "limit": 10,
            "after": "previous-broadcast-id",
        }
        broadcasts: resend.Broadcasts.ListResponse = resend.Broadcasts.list(
            params=params
        )
        assert broadcasts["object"] == "list"
        assert broadcasts["has_more"] is True
        assert len(broadcasts["data"]) == 2
        assert broadcasts["data"][0]["id"] == "broadcast-1"
        assert broadcasts["data"][1]["id"] == "broadcast-2"

    def test_broadcasts_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "broadcast-3",
                        "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "status": "draft",
                        "created_at": "2024-10-01 15:13:31.723+00",
                        "scheduled_at": None,
                        "sent_at": None,
                    }
                ],
            }
        )

        params: resend.Broadcasts.ListParams = {
            "limit": 5,
            "before": "later-broadcast-id",
        }
        broadcasts: resend.Broadcasts.ListResponse = resend.Broadcasts.list(
            params=params
        )
        assert broadcasts["object"] == "list"
        assert broadcasts["has_more"] is False
        assert len(broadcasts["data"]) == 1
        assert broadcasts["data"][0]["id"] == "broadcast-3"

    def test_broadcasts_recipients(self) -> None:
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
            "type": "delivered",
        }
        recipients: resend.Broadcasts.RecipientsResponse = resend.Broadcasts.recipients(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf", params
        )
        assert recipients["object"] == "list"
        assert recipients["has_more"] is False
        assert len(recipients["data"]) == 1

        recipient = recipients["data"][0]
        assert recipient["id"] == "b2Zmc2V0OjA"
        assert recipient["contact_id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert recipient["email"] == "carter@example.com"

    def test_broadcasts_recipients_opened_has_count(self) -> None:
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
            "type": "opened",
        }
        recipients = resend.Broadcasts.recipients(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf", params
        )
        recipient = recipients["data"][0]
        assert recipient["contact_id"] is None
        assert recipient["count"] == 3

    def test_broadcasts_recipients_clicked_has_clicked_links(self) -> None:
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
            "type": "clicked",
            "email": "carter",
            "limit": 10,
        }
        recipients = resend.Broadcasts.recipients(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf", params
        )
        recipient = recipients["data"][0]
        assert recipient["count"] == 2
        assert recipient["clicked_links"] == [
            {"url": "https://resend.com/pricing", "clicks": 2}
        ]

    def test_broadcasts_recipients_bounced_has_bounce_type(self) -> None:
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
            "type": "bounced",
            "bounce_type": "permanent",
        }
        recipients = resend.Broadcasts.recipients(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf", params
        )
        recipient = recipients["data"][0]
        assert recipient["bounce_type"] == "permanent"

    def test_broadcasts_recipients_raise_exception_when_not_found(self) -> None:
        self.set_mock_json(
            {
                "statusCode": 404,
                "name": "not_found",
                "message": "Broadcast not found",
            }
        )

        params: resend.Broadcasts.RecipientsParams = {
            "type": "sent",
        }
        with self.assertRaises(ResendError):
            _ = resend.Broadcasts.recipients("does-not-exist", params)

    def test_broadcasts_clicked_links(self) -> None:
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
            resend.Broadcasts.clicked_links("559ac32e-9ef5-46fb-82a1-b76b840c0f7b")
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

    def test_broadcasts_clicked_links_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "b2Zmc2V0OjA",
                        "url": "https://resend.com/pricing",
                        "clicks": 42,
                        "unique_clicks": 30,
                    },
                ],
            }
        )

        params: resend.Broadcasts.ListClickedLinksParams = {
            "limit": 1,
            "after": "cursor-value",
        }
        clicked_links: resend.Broadcasts.ListClickedLinksResponse = (
            resend.Broadcasts.clicked_links(
                "559ac32e-9ef5-46fb-82a1-b76b840c0f7b", params=params
            )
        )
        assert clicked_links["object"] == "list"
        assert clicked_links["has_more"] is True
        assert len(clicked_links["data"]) == 1
        assert clicked_links["data"][0]["id"] == "b2Zmc2V0OjA"

    def test_broadcasts_clicked_links_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [],
            }
        )

        params: resend.Broadcasts.ListClickedLinksParams = {
            "limit": 1,
            "before": "cursor-value",
        }
        clicked_links: resend.Broadcasts.ListClickedLinksResponse = (
            resend.Broadcasts.clicked_links(
                "559ac32e-9ef5-46fb-82a1-b76b840c0f7b", params=params
            )
        )
        assert clicked_links["object"] == "list"
        assert clicked_links["has_more"] is False
        assert len(clicked_links["data"]) == 0
