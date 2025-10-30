import resend
from resend import ContactsTopics
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendContactTopics(ResendBaseTest):
    def test_contact_topics_list_by_id(self) -> None:
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

        response: ContactsTopics.ListResponse = resend.Contacts.Topics.list(
            contact_id="cont_456"
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert response["data"][0]["id"] == "topic_123"
        assert response["data"][0]["name"] == "Newsletter"
        assert response["data"][0]["subscription"] == "opt_in"

    def test_contact_topics_list_by_email(self) -> None:
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

        response: ContactsTopics.ListResponse = resend.Contacts.Topics.list(
            email="user@example.com"
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert response["data"][0]["id"] == "topic_123"

    def test_contact_topics_list_with_pagination(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "topic_1",
                        "name": "Newsletter",
                        "description": "Weekly newsletter",
                        "subscription": "opt_in",
                    },
                    {
                        "id": "topic_2",
                        "name": "Updates",
                        "description": "Product updates",
                        "subscription": "opt_out",
                    },
                ],
            }
        )

        params: ContactsTopics.ListParams = {
            "limit": 10,
            "after": "topic_0",
        }
        response: ContactsTopics.ListResponse = resend.Contacts.Topics.list(
            contact_id="cont_456", params=params
        )
        assert response["object"] == "list"
        assert response["has_more"] is True
        assert len(response["data"]) == 2
        assert response["data"][0]["id"] == "topic_1"
        assert response["data"][1]["id"] == "topic_2"

    def test_contact_topics_list_raises_when_no_contact_identifier(self) -> None:
        resend.api_key = "re_123"

        with self.assertRaises(ValueError) as context:
            resend.Contacts.Topics.list()

        self.assertEqual("contact_id or email must be provided", str(context.exception))

    def test_should_list_contact_topics_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.Topics.list(contact_id="cont_456")

    def test_contact_topics_update_by_id(self) -> None:
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
        response: ContactsTopics.UpdateResponse = resend.Contacts.Topics.update(params)
        assert response["id"] == "cont_456"

    def test_contact_topics_update_by_email(self) -> None:
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
        response: ContactsTopics.UpdateResponse = resend.Contacts.Topics.update(params)
        assert response["id"] == "cont_456"

    def test_contact_topics_update_raises_when_no_contact_identifier(self) -> None:
        resend.api_key = "re_123"

        params: ContactsTopics.UpdateParams = {
            "topics": [
                {"id": "topic_1", "subscription": "opt_in"},
            ],
        }

        with self.assertRaises(ValueError) as context:
            resend.Contacts.Topics.update(params)

        self.assertEqual("id or email must be provided", str(context.exception))

    def test_should_update_contact_topics_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: ContactsTopics.UpdateParams = {
            "id": "cont_456",
            "topics": [
                {"id": "topic_1", "subscription": "opt_in"},
            ],
        }
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.Topics.update(params)
