import resend
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResponseDict(ResendBaseTest):

    def test_list_response_supports_dict_access(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "att-1",
                        "filename": "avatar.png",
                        "content_type": "image/png",
                        "content_disposition": "inline",
                        "size": 1024,
                    },
                ],
            }
        )

        attachments = resend.Emails.Receiving.Attachments.list(email_id="test-email-id")
        assert attachments["object"] == "list"
        assert attachments["has_more"] is False
        assert len(attachments["data"]) == 1
        assert attachments["data"][0]["id"] == "att-1"

    def test_list_response_supports_attribute_access(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "att-1",
                        "filename": "avatar.png",
                        "content_type": "image/png",
                        "content_disposition": "inline",
                        "size": 1024,
                    },
                ],
            }
        )

        attachments = resend.Emails.Receiving.Attachments.list(email_id="test-email-id")
        assert attachments.object == "list"  # type: ignore[attr-defined]
        assert attachments.has_more is False  # type: ignore[attr-defined]
        assert len(attachments.data) == 1  # type: ignore[attr-defined]
        assert attachments.data[0]["id"] == "att-1"  # type: ignore[attr-defined]

    def test_attribute_access_raises_for_missing_key(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [],
            }
        )

        attachments = resend.Emails.Receiving.Attachments.list(email_id="test-email-id")
        with self.assertRaises(AttributeError):
            _ = attachments.nonexistent  # type: ignore[attr-defined]

    def test_single_response_supports_attribute_access(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )

        params: resend.Emails.SendParams = {
            "from": "from@email.io",
            "to": ["to@email.io"],
            "subject": "subject",
            "html": "<p>Hello</p>",
        }
        email = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert email.id == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"  # type: ignore[attr-defined]
