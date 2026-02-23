import pytest

import resend
from resend import EmailsReceiving
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendReceivingAsync(AsyncResendBaseTest):
    async def test_receiving_get_async(self) -> None:
        self.set_mock_json(
            {
                "id": "67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
                "object": "received_email",
                "from": "sender@example.com",
                "to": ["recipient@example.com"],
                "subject": "Test subject",
                "created_at": "2024-01-01T00:00:00Z",
            }
        )

        email: resend.ReceivedEmail = await resend.Emails.Receiving.get_async(
            email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
        )
        assert email["id"] == "67d9bcdb-5a02-42d7-8da9-0d6feea18cff"
        assert email["object"] == "received_email"

    async def test_should_get_receiving_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Emails.Receiving.get_async(
                email_id="67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
            )

    async def test_receiving_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "67d9bcdb-5a02-42d7-8da9-0d6feea18cff",
                        "from": "sender@example.com",
                        "to": ["recipient@example.com"],
                        "subject": "Test subject",
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ],
            }
        )

        emails: EmailsReceiving.ListResponse = (
            await resend.Emails.Receiving.list_async()
        )
        assert emails["object"] == "list"
        assert emails["has_more"] is True
        assert len(emails["data"]) == 1
        assert emails["data"][0]["id"] == "67d9bcdb-5a02-42d7-8da9-0d6feea18cff"

    async def test_should_list_receiving_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Emails.Receiving.list_async()

    async def test_receiving_attachments_get_async(self) -> None:
        self.set_mock_json(
            {
                "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
                "object": "attachment",
                "filename": "avatar.png",
                "content_type": "image/png",
                "content_disposition": "inline",
                "content_id": "img001",
                "download_url": "https://inbound-cdn.resend.com/test/attachments/test-id",
                "expires_at": "2025-10-17T14:29:41.521Z",
            }
        )

        attachment: resend.EmailAttachmentDetails = (
            await resend.Emails.Receiving.Attachments.get_async(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                attachment_id="2a0c9ce0-3112-4728-976e-47ddcd16a318",
            )
        )
        assert attachment["id"] == "2a0c9ce0-3112-4728-976e-47ddcd16a318"
        assert attachment["object"] == "attachment"
        assert attachment["filename"] == "avatar.png"

    async def test_should_get_receiving_attachment_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Emails.Receiving.Attachments.get_async(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                attachment_id="2a0c9ce0-3112-4728-976e-47ddcd16a318",
            )

    async def test_receiving_attachments_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
                        "filename": "avatar.png",
                        "content_type": "image/png",
                        "content_disposition": "inline",
                        "content_id": "img001",
                        "size": 1024,
                    },
                    {
                        "id": "3b1d0df1-4223-5839-a87f-58eecd27b429",
                        "filename": "document.pdf",
                        "content_type": "application/pdf",
                        "content_disposition": "attachment",
                        "size": 2048,
                    },
                ],
            }
        )

        attachments: EmailsReceiving.Attachments.ListResponse = (
            await resend.Emails.Receiving.Attachments.list_async(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
            )
        )
        assert attachments["object"] == "list"
        assert attachments["has_more"] is False
        assert len(attachments["data"]) == 2
        assert attachments["data"][0]["id"] == "2a0c9ce0-3112-4728-976e-47ddcd16a318"

    async def test_should_list_receiving_attachments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Emails.Receiving.Attachments.list_async(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
            )
