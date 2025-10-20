import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendAttachments(ResendBaseTest):

    def test_receiving_get_attachment(self) -> None:
        self.set_mock_json(
            {
                "object": "attachment",
                "data": {
                    "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
                    "filename": "avatar.png",
                    "content_type": "image/png",
                    "content_disposition": "inline",
                    "content_id": "img001",
                    "download_url": "https://inbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
                    "expires_at": "2025-10-17T14:29:41.521Z",
                },
            }
        )

        attachment: resend.ReceivedEmailAttachmentDetails = (
            resend.Attachments.Receiving.get(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                attachment_id="2a0c9ce0-3112-4728-976e-47ddcd16a318",
            )
        )
        assert attachment["id"] == "2a0c9ce0-3112-4728-976e-47ddcd16a318"
        assert attachment["object"] == "attachment"
        assert attachment["filename"] == "avatar.png"
        assert attachment["content_type"] == "image/png"
        assert attachment["content_disposition"] == "inline"
        assert attachment["content_id"] == "img001"
        assert "https://inbound-cdn.resend.com" in attachment["download_url"]
        assert attachment["expires_at"] == "2025-10-17T14:29:41.521Z"

    def test_receiving_get_attachment_without_content_id(self) -> None:
        self.set_mock_json(
            {
                "object": "attachment",
                "data": {
                    "id": "3b1c9ce0-4223-5839-a87f-58eecd27b429",
                    "filename": "document.pdf",
                    "content_type": "application/pdf",
                    "content_disposition": "attachment",
                    "download_url": "https://inbound-cdn.resend.com/test-email/attachments/test-attachment",
                    "expires_at": "2025-10-18T10:00:00.000Z",
                },
            }
        )

        attachment: resend.ReceivedEmailAttachmentDetails = (
            resend.Attachments.Receiving.get(
                email_id="test-email-id",
                attachment_id="3b1c9ce0-4223-5839-a87f-58eecd27b429",
            )
        )
        assert attachment["id"] == "3b1c9ce0-4223-5839-a87f-58eecd27b429"
        assert attachment["filename"] == "document.pdf"
        assert attachment["content_type"] == "application/pdf"
        assert attachment["content_disposition"] == "attachment"
        assert "content_id" not in attachment or attachment.get("content_id") is None

    def test_should_receiving_get_attachment_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Attachments.Receiving.get(
                email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                attachment_id="2a0c9ce0-3112-4728-976e-47ddcd16a318",
            )

    def test_receiving_list_attachments(self) -> None:
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

        list_params: resend.Attachments.Receiving.ListParams = {
            "email_id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        }
        attachments: resend.Attachments.Receiving.ListResponse = (
            resend.Attachments.Receiving.list(params=list_params)
        )

        assert attachments["object"] == "list"
        assert attachments["has_more"] == False
        assert len(attachments["data"]) == 2
        assert attachments["data"][0]["id"] == "2a0c9ce0-3112-4728-976e-47ddcd16a318"
        assert attachments["data"][0]["filename"] == "avatar.png"
        assert attachments["data"][0]["size"] == 1024
        assert attachments["data"][1]["id"] == "3b1d0df1-4223-5839-a87f-58eecd27b429"
        assert attachments["data"][1]["filename"] == "document.pdf"

    def test_receiving_list_attachments_with_pagination(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
                        "filename": "avatar.png",
                        "content_type": "image/png",
                        "content_disposition": "inline",
                        "size": 1024,
                    },
                ],
            }
        )

        list_params: resend.Attachments.Receiving.ListParams = {
            "email_id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
            "limit": 1,
        }
        attachments: resend.Attachments.Receiving.ListResponse = (
            resend.Attachments.Receiving.list(params=list_params)
        )

        assert attachments["object"] == "list"
        assert attachments["has_more"] == True
        assert len(attachments["data"]) == 1

    def test_receiving_list_attachments_empty(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [],
            }
        )

        list_params: resend.Attachments.Receiving.ListParams = {
            "email_id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        }
        attachments: resend.Attachments.Receiving.ListResponse = (
            resend.Attachments.Receiving.list(params=list_params)
        )

        assert attachments["object"] == "list"
        assert len(attachments["data"]) == 0
        assert attachments["has_more"] == False

    def test_should_receiving_list_attachments_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        list_params: resend.Attachments.Receiving.ListParams = {
            "email_id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Attachments.Receiving.list(params=list_params)
