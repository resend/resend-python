from unittest.mock import MagicMock

import resend
from resend.exceptions import NoContentError, ResendError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendEmail(ResendBaseTest):

    def test_email_send_with_from(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )
        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "subject": "subject",
            "html": "html",
        }
        email: resend.Emails.SendResponse = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_should_send_email_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "subject": "subject",
            "html": "html",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Emails.send(params)

    def test_email_get(self) -> None:
        self.set_mock_json(
            {
                "object": "email",
                "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                "to": ["james@bond.com"],
                "from": "onboarding@resend.dev",
                "created_at": "2023-04-03T22:13:42.674981+00:00",
                "subject": "Hello World",
                "html": "Congrats on sending your <strong>first email</strong>!",
                "text": None,
                "bcc": [None],
                "cc": [None],
                "reply_to": [None],
                "last_event": "delivered",
            }
        )

        email: resend.Email = resend.Emails.get(
            email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        )
        assert email["id"] == "4ef9a417-02e9-4d39-ad75-9611e0fcc33c"

    def test_should_get_email_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.get(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
            )

    def test_email_response_html(self) -> None:
        self.set_magic_mock_obj(
            MagicMock(
                status_code=200,
                headers={"content-type": "text/html; charset=utf-8"},
                text="<strong>hello, world!</strong>",
            )
        )
        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "subject": "subject",
            "html": "html",
        }
        try:
            _ = resend.Emails.send(params)
        except ResendError as e:
            assert e.message == "Failed to parse Resend API response. Please try again."

    def test_update_email(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )
        update_params: resend.Emails.UpdateParams = {
            "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            "scheduled_at": "2024-09-07T11:52:01.858Z",
        }
        updated_email: resend.Emails.UpdateEmailResponse = resend.Emails.update(
            params=update_params
        )
        assert updated_email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_cancel_scheduled_email(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )
        email: resend.Emails.CancelScheduledEmailResponse = resend.Emails.cancel(
            email_id="49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_email_send_with_attachment(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )

        attachment: resend.Attachment = {
            "filename": "test.pdf",
            "content": [1, 2, 3, 4, 5],
            "content_type": "application/pdf",
        }

        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "subject": "subject",
            "html": "html",
            "attachments": [attachment],
        }
        email: resend.Emails.SendResponse = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_email_send_with_inline_attachment(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )

        attachment: resend.Attachment = {
            "filename": "image.png",
            "content": [1, 2, 3, 4, 5],
            "content_type": "image/png",
            "content_id": "my-image",
        }

        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "subject": "subject",
            "html": '<img src="cid:my-image" />',
            "attachments": [attachment],
        }
        email: resend.Emails.SendResponse = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_email_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "data": [
                    {
                        "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                        "to": ["james@bond.com"],
                        "from": "onboarding@resend.dev",
                        "created_at": "2023-04-03T22:13:42.674981+00:00",
                        "subject": "Hello World",
                        "html": "Congrats on sending your <strong>first email</strong>!",
                        "text": None,
                        "bcc": [None],
                        "cc": [None],
                        "reply_to": [None],
                        "last_event": "delivered",
                    },
                    {
                        "id": "5ef9a417-02e9-4d39-ad75-9611e0fcc33d",
                        "to": ["test@example.com"],
                        "from": "hello@resend.dev",
                        "created_at": "2023-04-04T10:15:42.674981+00:00",
                        "subject": "Test Email",
                        "html": "This is a test email",
                        "text": "This is a test email",
                        "bcc": [None],
                        "cc": [None],
                        "reply_to": [None],
                        "last_event": "sent",
                    },
                ],
                "has_more": True,
            }
        )

        emails: resend.Emails.ListResponse = resend.Emails.list()
        assert emails["object"] == "list"
        assert len(emails["data"]) == 2
        assert emails["has_more"] == True
        assert emails["data"][0]["id"] == "4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
        assert emails["data"][1]["id"] == "5ef9a417-02e9-4d39-ad75-9611e0fcc33d"

    def test_email_list_with_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "data": [
                    {
                        "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                        "to": ["james@bond.com"],
                        "from": "onboarding@resend.dev",
                        "created_at": "2023-04-03T22:13:42.674981+00:00",
                        "subject": "Hello World",
                        "html": "Congrats on sending your <strong>first email</strong>!",
                        "text": None,
                        "bcc": [None],
                        "cc": [None],
                        "reply_to": [None],
                        "last_event": "delivered",
                    },
                ],
                "has_more": False,
            }
        )

        list_params: resend.Emails.ListParams = {
            "limit": 10,
            "after": "cursor123",
        }
        emails: resend.Emails.ListResponse = resend.Emails.list(params=list_params)
        assert emails["object"] == "list"
        assert len(emails["data"]) == 1
        assert emails["has_more"] == False

    def test_email_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "data": [],
                "has_more": False,
            }
        )

        list_params: resend.Emails.ListParams = {
            "limit": 5,
            "before": "cursor456",
        }
        emails: resend.Emails.ListResponse = resend.Emails.list(params=list_params)
        assert emails["object"] == "list"
        assert len(emails["data"]) == 0
        assert emails["has_more"] == False

    def test_should_list_email_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.list()

    def test_receiving_get(self) -> None:
        self.set_mock_json(
            {
                "object": "inbound",
                "id": "67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
                "to": ["received@example.com"],
                "from": "sender@example.com",
                "created_at": "2023-04-07T23:13:52.669661+00:00",
                "subject": "Test inbound email",
                "html": "<p>hello world</p>",
                "text": "hello world",
                "bcc": None,
                "cc": ["cc@example.com"],
                "reply_to": ["reply@example.com"],
                "headers": {
                    "example": "value",
                },
                "attachments": [
                    {
                        "id": "att_123",
                        "filename": "document.pdf",
                        "content_type": "application/pdf",
                        "content_id": "cid_123",
                        "content_disposition": "attachment",
                    }
                ],
            }
        )

        email: resend.ReceivedEmail = resend.Emails.Receiving.get(
            email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
        )
        assert email["id"] == "67d9bcdb-5a02-42d7-8da9-0d6feea18cff"
        assert email["object"] == "inbound"
        assert email["to"] == ["received@example.com"]
        assert email["from"] == "sender@example.com"
        assert email["subject"] == "Test inbound email"
        assert email["html"] == "<p>hello world</p>"
        assert email["text"] == "hello world"
        assert email["bcc"] is None
        assert email["cc"] == ["cc@example.com"]
        assert email["reply_to"] == ["reply@example.com"]
        assert email["headers"]["example"] == "value"
        assert len(email["attachments"]) == 1
        assert email["attachments"][0]["id"] == "att_123"
        assert email["attachments"][0]["filename"] == "document.pdf"

    def test_receiving_get_with_no_attachments(self) -> None:
        self.set_mock_json(
            {
                "object": "inbound",
                "id": "67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
                "to": ["received@example.com"],
                "from": "sender@example.com",
                "created_at": "2023-04-07T23:13:52.669661+00:00",
                "subject": "Test inbound email",
                "html": None,
                "text": "hello world",
                "bcc": None,
                "cc": None,
                "reply_to": None,
                "headers": {},
                "attachments": [],
            }
        )

        email: resend.ReceivedEmail = resend.Emails.Receiving.get(
            email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
        )
        assert email["id"] == "67d9bcdb-5a02-42d7-8da9-0d6feea18cff"
        assert email["html"] is None
        assert email["bcc"] is None
        assert email["cc"] is None
        assert email["reply_to"] is None
        assert len(email["attachments"]) == 0

    def test_should_receiving_get_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.Receiving.get(
                email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
            )
