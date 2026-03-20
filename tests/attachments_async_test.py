import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendAttachmentsAsync(AsyncResendBaseTest):
    async def test_sent_email_attachments_get_async(self) -> None:
        self.set_mock_json(
            {
                "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
                "object": "attachment",
                "filename": "avatar.png",
                "content_type": "image/png",
                "content_disposition": "inline",
                "content_id": "img001",
                "download_url": "https://cdn.resend.com/emails/test/attachments/test-id",
                "expires_at": "2025-10-17T14:29:41.521Z",
            }
        )

        attachment: resend.EmailAttachmentDetails = (
            await resend.Emails.Attachments.get_async(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                attachment_id="2a0c9ce0-3112-4728-976e-47ddcd16a318",
            )
        )
        assert attachment["id"] == "2a0c9ce0-3112-4728-976e-47ddcd16a318"
        assert attachment["object"] == "attachment"
        assert attachment["filename"] == "avatar.png"

    async def test_should_get_sent_email_attachment_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Emails.Attachments.get_async(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                attachment_id="2a0c9ce0-3112-4728-976e-47ddcd16a318",
            )

    async def test_sent_email_attachments_list_async(self) -> None:
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
                        "size": 1024,
                    }
                ],
            }
        )

        attachments = await resend.Emails.Attachments.list_async(
            email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
        )
        assert attachments["object"] == "list"
        assert attachments["has_more"] is False
        assert len(attachments["data"]) == 1
        assert attachments["data"][0]["id"] == "2a0c9ce0-3112-4728-976e-47ddcd16a318"

    async def test_should_list_sent_email_attachments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Emails.Attachments.list_async(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
            )
