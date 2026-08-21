from unittest.mock import Mock

import resend
from resend import EmailsReceiving
from resend.exceptions import NoContentError, ResendError, ValidationError
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
                "message_id": "<111-222-333@email.example.com>",
                "to": ["james@bond.com"],
                "from": "onboarding@resend.dev",
                "created_at": "2023-04-03 22:13:42.674981+00",
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
        assert email["message_id"] == "<111-222-333@email.example.com>"

    def test_should_get_email_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.get(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
            )

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

    def test_share_email_default_expires_in(self) -> None:
        self.set_mock_json(
            {
                "object": "email",
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
                "url": "https://resend.com/share/49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )
        shared_email: resend.Emails.ShareEmailResponse = resend.Emails.share(
            email_id="49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )
        assert shared_email["object"] == "email"
        assert shared_email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert (
            shared_email["url"]
            == "https://resend.com/share/49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )

    def test_share_email_with_custom_expires_in(self) -> None:
        self.set_mock_json(
            {
                "object": "email",
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
                "url": "https://resend.com/share/49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )
        share_params: resend.Emails.ShareParams = {
            "expires_in": "10m",
        }
        shared_email: resend.Emails.ShareEmailResponse = resend.Emails.share(
            email_id="49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            params=share_params,
        )
        assert shared_email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert (
            shared_email["url"]
            == "https://resend.com/share/49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )

    def test_share_email_with_malformed_expires_in_raises_validation_error(
        self,
    ) -> None:
        self.set_mock_json(
            {
                "statusCode": 422,
                "name": "validation_error",
                "message": "expires_in must not exceed 48 hours",
            }
        )
        share_params: resend.Emails.ShareParams = {
            "expires_in": "72h",
        }
        with self.assertRaises(ValidationError):
            _ = resend.Emails.share(
                email_id="49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
                params=share_params,
            )

    def test_share_email_with_unknown_id_raises_error(self) -> None:
        self.set_mock_json(
            {
                "statusCode": 404,
                "name": "not_found",
                "message": "Email not found",
            }
        )
        with self.assertRaises(ResendError):
            _ = resend.Emails.share(email_id="does-not-exist")

    def test_should_share_email_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.share(
                email_id="49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            )

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
                        "message_id": "<111-222-333@email.example.com>",
                        "to": ["james@bond.com"],
                        "from": "onboarding@resend.dev",
                        "created_at": "2023-04-03 22:13:42.674981+00",
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
                        "message_id": "<222-333-444@email.example.com>",
                        "to": ["test@example.com"],
                        "from": "hello@resend.dev",
                        "created_at": "2023-04-04 10:15:42.674981+00",
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
        assert emails["data"][0]["message_id"] == "<111-222-333@email.example.com>"
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
                        "created_at": "2023-04-03 22:13:42.674981+00",
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
                "created_at": "2023-04-07 23:13:52.669661+00",
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
                        "size": 4096,
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
                "created_at": "2023-04-07 23:13:52.669661+00",
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

    def test_receiving_get_with_nullable_attachment_fields(self) -> None:
        # Inbound MIME parts (S/MIME signatures, calendar invites) can return
        # null for filename, content_id, and content_disposition.
        # See: https://linear.app/resend/issue/DEV-934
        self.set_mock_json(
            {
                "object": "inbound",
                "id": "67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
                "to": ["received@example.com"],
                "from": "sender@example.com",
                "created_at": "2023-04-07 23:13:52.669661+00",
                "subject": "Signed inbound email",
                "html": None,
                "text": "hello world",
                "bcc": None,
                "cc": None,
                "reply_to": None,
                "headers": {},
                "message_id": "<msg@example.com>",
                "attachments": [
                    {
                        "id": "f5e32216-3017-4118-97d5-5c84d991bf98",
                        "filename": "smime.p7s",
                        "content_type": "application/pkcs7-signature",
                        "content_id": None,
                        "content_disposition": "attachment",
                        "size": 1361,
                    },
                    {
                        "id": "68136802-3577-4911-a7d2-b303e61261ac",
                        "filename": None,
                        "content_type": "text/calendar",
                        "content_id": None,
                        "content_disposition": None,
                        "size": 1152,
                    },
                ],
            }
        )

        email: resend.ReceivedEmail = resend.Emails.Receiving.get(
            email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
        )
        assert len(email["attachments"]) == 2

        smime = email["attachments"][0]
        assert smime["filename"] == "smime.p7s"
        assert smime["content_disposition"] == "attachment"
        assert smime["content_id"] is None

        calendar = email["attachments"][1]
        assert calendar["filename"] is None
        assert calendar["content_disposition"] is None
        assert calendar["content_id"] is None

    def test_receiving_get_with_html_format_cid(self) -> None:
        self.set_mock_json(
            {
                "object": "inbound",
                "id": "67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
                "to": ["received@example.com"],
                "from": "sender@example.com",
                "created_at": "2023-04-07 23:13:52.669661+00",
                "subject": "Test inbound email",
                "html": '<img src="cid:img001" />',
                "text": "hello world",
                "bcc": None,
                "cc": None,
                "reply_to": None,
                "attachments": [],
            }
        )

        params: EmailsReceiving.GetParams = {"html_format": "cid"}
        email: resend.ReceivedEmail = resend.Emails.Receiving.get(
            email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
            params=params,
        )
        assert email["id"] == "67d9bcdb-5a02-42d7-8da9-0d6feea18cff"
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/receiving/67d9bcdb-5a02-42d7-8da9-0d6feea18cff?html_format=cid"
        )

    def test_receiving_get_with_html_format_data_uri(self) -> None:
        self.set_mock_json(
            {
                "object": "inbound",
                "id": "67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
                "to": ["received@example.com"],
                "from": "sender@example.com",
                "created_at": "2023-04-07 23:13:52.669661+00",
                "subject": "Test inbound email",
                "html": '<img src="data:image/png;base64,abc" />',
                "text": "hello world",
                "bcc": None,
                "cc": None,
                "reply_to": None,
                "attachments": [],
            }
        )

        params: EmailsReceiving.GetParams = {"html_format": "data_uri"}
        email: resend.ReceivedEmail = resend.Emails.Receiving.get(
            email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
            params=params,
        )
        assert email["id"] == "67d9bcdb-5a02-42d7-8da9-0d6feea18cff"
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/receiving/67d9bcdb-5a02-42d7-8da9-0d6feea18cff?html_format=data_uri"
        )

    def test_should_receiving_get_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.Receiving.get(
                email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
            )

    def test_receiving_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "a39999a6-88e3-48b1-888b-beaabcde1b33",
                        "to": ["recipient@example.com"],
                        "from": "sender@example.com",
                        "created_at": "2025-10-09 14:37:40.951732+00",
                        "subject": "Hello World",
                        "bcc": [],
                        "cc": [],
                        "reply_to": [],
                        "message_id": "<111-222-333@email.provider.example.com>",
                        "attachments": [
                            {
                                "filename": "example.txt",
                                "content_type": "text/plain",
                                "content_id": None,
                                "content_disposition": "attachment",
                                "id": "47e999c7-c89c-4999-bf32-aaaaa1c3ff21",
                                "size": 13,
                            }
                        ],
                    },
                    {
                        "id": "b49999a6-99e3-59b1-999b-ceaabcde2c44",
                        "to": ["another@example.com"],
                        "from": "sender2@example.com",
                        "created_at": "2025-10-10 10:20:30.123456+00",
                        "subject": "Test Email",
                        "bcc": None,
                        "cc": ["cc@example.com"],
                        "reply_to": None,
                        "message_id": "<222-333-444@email.provider.example.com>",
                        "attachments": [],
                    },
                ],
            }
        )

        emails: EmailsReceiving.ListResponse = resend.Emails.Receiving.list()
        assert emails["object"] == "list"
        assert emails["has_more"] == True
        assert len(emails["data"]) == 2
        assert emails["data"][0]["id"] == "a39999a6-88e3-48b1-888b-beaabcde1b33"
        assert emails["data"][0]["subject"] == "Hello World"
        assert len(emails["data"][0]["attachments"]) == 1
        assert emails["data"][0]["attachments"][0]["size"] == 13
        assert emails["data"][1]["id"] == "b49999a6-99e3-59b1-999b-ceaabcde2c44"

    def test_receiving_list_with_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "a39999a6-88e3-48b1-888b-beaabcde1b33",
                        "to": ["recipient@example.com"],
                        "from": "sender@example.com",
                        "created_at": "2025-10-09 14:37:40.951732+00",
                        "subject": "Hello World",
                        "bcc": None,
                        "cc": None,
                        "reply_to": None,
                        "message_id": "<111-222-333@email.provider.example.com>",
                        "attachments": [],
                    }
                ],
            }
        )

        list_params: EmailsReceiving.ListParams = {
            "limit": 10,
            "after": "cursor123",
        }
        emails: EmailsReceiving.ListResponse = resend.Emails.Receiving.list(
            params=list_params
        )
        assert emails["object"] == "list"
        assert len(emails["data"]) == 1
        assert emails["has_more"] == False

    def test_receiving_list_empty(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [],
            }
        )

        emails: EmailsReceiving.ListResponse = resend.Emails.Receiving.list()
        assert emails["object"] == "list"
        assert len(emails["data"]) == 0
        assert emails["has_more"] == False

    def test_should_receiving_list_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.Receiving.list()

    def test_email_send_with_template(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )

        template: resend.EmailTemplate = {
            "id": "template_12345",
        }

        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "template": template,
        }
        email: resend.Emails.SendResponse = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_email_send_with_template_and_variables(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )

        template: resend.EmailTemplate = {
            "id": "template_12345",
            "variables": {
                "name": "John Doe",
                "age": 30,
            },
        }

        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "template": template,
        }
        email: resend.Emails.SendResponse = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_email_send_with_custom_headers(self) -> None:
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
            "headers": {
                "X-Entity-Ref-ID": "123456",
            },
        }
        email: resend.Emails.SendResponse = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_metrics_with_no_params(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-02T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered", "opened"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 100, "opened": 40},
            }
        )
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics()
        assert metrics["object"] == "metrics"
        assert metrics["totals"]["delivered"] == 100
        assert "data" not in metrics
        self.mock.assert_called_with(url="https://api.resend.com/emails/metrics")

    def test_metrics_with_period_dimension(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": ["period"],
                "granularity": "daily",
                "totals": {"delivered": 100},
                "data": [
                    {"period": "2026-07-01", "delivered": 10},
                    {"period": "2026-07-02", "delivered": 20},
                ],
            }
        )
        params: resend.Emails.MetricsParams = {"dimensions": ["period"]}
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["dimensions"] == ["period"]
        assert metrics["data"][0]["period"] == "2026-07-01"
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?dimensions=period"
        )

    def test_metrics_with_domain_dimension(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": ["domain"],
                "granularity": "daily",
                "totals": {"delivered": 100},
                "data": [
                    {
                        "domain_id": "d68a4265-d33b-4658-b9e6-c9d0c5b0e4a3",
                        "domain_name": "example.com",
                        "delivered": 100,
                    },
                ],
            }
        )
        params: resend.Emails.MetricsParams = {"dimensions": ["domain"]}
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["dimensions"] == ["domain"]
        assert metrics["data"][0]["domain_name"] == "example.com"
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?dimensions=domain"
        )

    def test_metrics_with_email_dimension(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": ["email"],
                "granularity": "daily",
                "totals": {"delivered": 1},
                "data": [
                    {
                        "email_id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                        "delivered": 1,
                    },
                ],
            }
        )
        params: resend.Emails.MetricsParams = {"dimensions": ["email"]}
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["dimensions"] == ["email"]
        assert metrics["data"][0]["email_id"] == "4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?dimensions=email"
        )

    def test_metrics_with_broadcast_dimension(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered", "opened"],
                "dimensions": ["broadcast"],
                "granularity": "daily",
                "totals": {"delivered": 100, "opened": 40},
                "data": [
                    {
                        "broadcast_id": "b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f",
                        "broadcast_name": "July Newsletter",
                        "delivered": 100,
                        "opened": 40,
                    },
                ],
            }
        )
        params: resend.Emails.MetricsParams = {"dimensions": ["broadcast"]}
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["dimensions"] == ["broadcast"]
        assert metrics["data"][0]["broadcast_name"] == "July Newsletter"
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?dimensions=broadcast"
        )

    def test_metrics_with_multiple_dimensions(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered", "opened"],
                "dimensions": ["period", "broadcast"],
                "granularity": "daily",
                "totals": {"delivered": 100, "opened": 40},
                "data": [
                    {
                        "period": "2026-07-01",
                        "broadcast_id": "b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f",
                        "broadcast_name": "July Newsletter",
                        "delivered": 10,
                        "opened": 4,
                    },
                ],
            }
        )
        params: resend.Emails.MetricsParams = {"dimensions": ["period", "broadcast"]}
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["dimensions"] == ["period", "broadcast"]
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?dimensions=period%2Cbroadcast"
        )

    def test_metrics_with_single_domain_id_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 50},
            }
        )
        params: resend.Emails.MetricsParams = {
            "domain_id": ["d68a4265-d33b-4658-b9e6-c9d0c5b0e4a3"],
        }
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["totals"]["delivered"] == 50
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?domain_id=d68a4265-d33b-4658-b9e6-c9d0c5b0e4a3"
        )

    def test_metrics_with_multiple_domain_id_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 90},
            }
        )
        params: resend.Emails.MetricsParams = {
            "domain_id": [
                "d68a4265-d33b-4658-b9e6-c9d0c5b0e4a3",
                "e79b5376-e44c-5769-c0f7-dae1d6c1f5b4",
            ],
        }
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["totals"]["delivered"] == 90
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?domain_id=d68a4265-d33b-4658-b9e6-c9d0c5b0e4a3%2Ce79b5376-e44c-5769-c0f7-dae1d6c1f5b4"
        )

    def test_metrics_with_single_email_id_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 1},
            }
        )
        params: resend.Emails.MetricsParams = {
            "email_id": ["4ef9a417-02e9-4d39-ad75-9611e0fcc33c"],
        }
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["totals"]["delivered"] == 1
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?email_id=4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
        )

    def test_metrics_with_multiple_email_id_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 2},
            }
        )
        params: resend.Emails.MetricsParams = {
            "email_id": [
                "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                "5ef9a417-02e9-4d39-ad75-9611e0fcc33d",
            ],
        }
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["totals"]["delivered"] == 2
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?email_id=4ef9a417-02e9-4d39-ad75-9611e0fcc33c%2C5ef9a417-02e9-4d39-ad75-9611e0fcc33d"
        )

    def test_metrics_with_single_broadcast_id_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 100},
            }
        )
        params: resend.Emails.MetricsParams = {
            "broadcast_id": ["b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f"],
        }
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["totals"]["delivered"] == 100
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?broadcast_id=b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f"
        )

    def test_metrics_with_multiple_broadcast_id_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 150},
            }
        )
        params: resend.Emails.MetricsParams = {
            "broadcast_id": [
                "b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f",
                "c4b7f7f3-a03c-5f3b-ac2c-2b3c4d5e6f70",
            ],
        }
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["totals"]["delivered"] == 150
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?broadcast_id=b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f%2Cc4b7f7f3-a03c-5f3b-ac2c-2b3c4d5e6f70"
        )

    def test_metrics_with_metrics_granularity_and_timezone(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered", "opened", "clicked"],
                "dimensions": ["period"],
                "granularity": "hourly",
                "totals": {"delivered": 100, "opened": 40, "clicked": 10},
                "data": [
                    {
                        "period": "2026-07-01T00:00:00.000Z",
                        "delivered": 5,
                        "opened": 2,
                        "clicked": 1,
                    },
                ],
            }
        )
        params: resend.Emails.MetricsParams = {
            "start_date": "2026-07-01",
            "end_date": "2026-07-08",
            "timezone": "America/New_York",
            "granularity": "hourly",
            "metrics": ["delivered", "opened", "clicked"],
            "dimensions": ["period"],
        }
        metrics: resend.Emails.MetricsResponse = resend.Emails.metrics(params=params)
        assert metrics["granularity"] == "hourly"
        assert metrics["metrics"] == ["delivered", "opened", "clicked"]
        self.mock.assert_called_with(
            url=(
                "https://api.resend.com/emails/metrics?"
                "start_date=2026-07-01&end_date=2026-07-08"
                "&timezone=America%2FNew_York&granularity=hourly"
                "&metrics=delivered%2Copened%2Cclicked&dimensions=period"
            )
        )

    def test_metrics_raises_when_email_and_broadcast_dimensions_combined(
        self,
    ) -> None:
        params: resend.Emails.MetricsParams = {
            "dimensions": ["email", "broadcast"],
        }
        try:
            resend.Emails.metrics(params=params)
            self.fail("expected ValueError")
        except ValueError as e:
            assert str(e) == (
                "the broadcast dimension/broadcast_id filter cannot be "
                "combined with the email dimension/email_id filter"
            )
        self.mock.assert_not_called()

    def test_metrics_raises_when_broadcast_dimension_combined_with_email_id(
        self,
    ) -> None:
        params: resend.Emails.MetricsParams = {
            "dimensions": ["broadcast"],
            "email_id": ["4dd369bc-aa82-4ff3-97de-514ae3000ee0"],
        }
        with self.assertRaises(ValueError):
            resend.Emails.metrics(params=params)
        self.mock.assert_not_called()

    def test_metrics_raises_when_email_dimension_combined_with_broadcast_id(
        self,
    ) -> None:
        params: resend.Emails.MetricsParams = {
            "dimensions": ["email"],
            "broadcast_id": ["b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f"],
        }
        with self.assertRaises(ValueError):
            resend.Emails.metrics(params=params)
        self.mock.assert_not_called()

    def test_metrics_raises_when_email_id_and_broadcast_id_combined(self) -> None:
        params: resend.Emails.MetricsParams = {
            "email_id": ["4dd369bc-aa82-4ff3-97de-514ae3000ee0"],
            "broadcast_id": ["b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f"],
        }
        with self.assertRaises(ValueError):
            resend.Emails.metrics(params=params)
        self.mock.assert_not_called()

    def test_should_metrics_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Emails.metrics()


import unittest as _unittest


class TestEmailHeadersRegression(_unittest.TestCase):
    """
    Tests that mock at the HTTP client level to exercise request.py's injection
    code. ResendBaseTest mocks make_request directly, which bypasses that code
    and would not have caught the v2.23.0 regression.
    """

    def setUp(self) -> None:
        resend.api_key = "re_123"

    def test_receiving_get_email_headers_not_overwritten_by_http_headers(self) -> None:
        mock_client = Mock()
        mock_client.request.return_value = (
            b'{"object":"inbound","id":"67d9bcdb-5a02-42d7-8da9-0d6feea18cff",'
            b'"to":["received@example.com"],"from":"sender@example.com",'
            b'"created_at":"2023-04-07 23:13:52.669661+00","subject":"Test",'
            b'"html":null,"text":"hello","bcc":null,"cc":null,"reply_to":null,'
            b'"message_id":"<msg123>","headers":{"X-Custom":"email-value"},'
            b'"attachments":[]}',
            200,
            {
                "content-type": "application/json",
                "x-request-id": "req_abc123",
            },
        )

        original_client = resend.default_http_client
        resend.default_http_client = mock_client

        try:
            email: resend.ReceivedEmail = resend.Emails.Receiving.get(
                email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
            )
            # Email MIME headers must survive the HTTP headers injection
            assert email["headers"] == {"X-Custom": "email-value"}
            # HTTP response headers are available separately
            assert email["http_headers"]["x-request-id"] == "req_abc123"
        finally:
            resend.default_http_client = original_client
