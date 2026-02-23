import resend
from resend import ContactsTopics
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendContactTopicsAsync(ResendBaseTest):
    async def test_contact_topics_list_async_by_id(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "topic_123",
                        "name": "Newsletter",
                        "description": "Weekly newsletter",
                        "subscription": "opt_in",
                    }
                ],
            }
        )

        response: ContactsTopics.ListResponse = await resend.Contacts.Topics.list_async(
            contact_id="cont_456"
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert response["data"][0]["id"] == "topic_123"
        assert response["data"][0]["name"] == "Newsletter"
        assert response["data"][0]["subscription"] == "opt_in"

    async def test_contact_topics_list_async_by_email(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "topic_123",
                        "name": "Newsletter",
                        "description": "Weekly newsletter",
                        "subscription": "opt_in",
                    }
                ],
            }
        )

        response: ContactsTopics.ListResponse = await resend.Contacts.Topics.list_async(
            email="user@example.com"
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert response["data"][0]["id"] == "topic_123"

    async def test_contact_topics_list_async_raises_when_no_contact_identifier(
        self,
    ) -> None:
        resend.api_key = "re_123"

        with self.assertRaises(ValueError) as context:
            await resend.Contacts.Topics.list_async()

        self.assertEqual("contact_id or email must be provided", str(context.exception))

    async def test_should_list_contact_topics_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.Contacts.Topics.list_async(contact_id="cont_456")

    async def test_contact_topics_update_async_by_id(self) -> None:
        self.set_mock_json(
            {
                "id": "cont_456",
            }
        )

        params: ContactsTopics.UpdateParams = {
            "id": "cont_456",
            "topics": [
                {"id": "topic_1", "subscription": "opt_in"},
                {"id": "topic_2", "subscription": "opt_out"},
            ],
        }
        response: ContactsTopics.UpdateResponse = (
            await resend.Contacts.Topics.update_async(params)
        )
        assert response["id"] == "cont_456"

    async def test_contact_topics_update_async_by_email(self) -> None:
        self.set_mock_json(
            {
                "id": "cont_456",
            }
        )

        params: ContactsTopics.UpdateParams = {
            "email": "user@example.com",
            "topics": [
                {"id": "topic_1", "subscription": "opt_in"},
            ],
        }
        response: ContactsTopics.UpdateResponse = (
            await resend.Contacts.Topics.update_async(params)
        )
        assert response["id"] == "cont_456"

    async def test_contact_topics_update_async_raises_when_no_contact_identifier(
        self,
    ) -> None:
        resend.api_key = "re_123"

        params: ContactsTopics.UpdateParams = {
            "topics": [
                {"id": "topic_1", "subscription": "opt_in"},
            ],
        }

        with self.assertRaises(ValueError) as context:
            await resend.Contacts.Topics.update_async(params)

        self.assertEqual("id or email must be provided", str(context.exception))

    async def test_should_update_contact_topics_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: ContactsTopics.UpdateParams = {
            "id": "cont_456",
            "topics": [
                {"id": "topic_1", "subscription": "opt_in"},
            ],
        }
        with self.assertRaises(NoContentError):
            _ = await resend.Contacts.Topics.update_async(params)
