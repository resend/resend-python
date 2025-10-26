import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendTopics(ResendBaseTest):
    def test_topics_create(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Topics.CreateParams = {
            "name": "Weekly Newsletter",
            "default_subscription": "opt_in",
        }
        topic = resend.Topics.create(params)
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_topics_create_with_description(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Topics.CreateParams = {
            "name": "Weekly Newsletter",
            "default_subscription": "opt_in",
            "description": "Subscribe to our weekly newsletter for updates",
        }
        topic = resend.Topics.create(params)
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_create_topics_raises_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Topics.CreateParams = {
            "name": "Weekly Newsletter",
            "default_subscription": "opt_in",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Topics.create(params)

    def test_topics_get(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "name": "Weekly Newsletter",
                "description": "Weekly newsletter for our subscribers",
                "default_subscription": "opt_in",
                "created_at": "2023-04-08T00:11:13.110779+00:00",
            }
        )

        topic = resend.Topics.get(id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e")
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert topic["name"] == "Weekly Newsletter"
        assert topic["description"] == "Weekly newsletter for our subscribers"
        assert topic["default_subscription"] == "opt_in"
        assert topic["created_at"] == "2023-04-08T00:11:13.110779+00:00"

    def test_should_get_topics_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Topics.get(id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e")

    def test_topics_update(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Topics.UpdateParams = {
            "name": "Monthly Newsletter",
            "description": "Monthly newsletter for our subscribers",
        }
        topic = resend.Topics.update(
            id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e", params=params
        )
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_topics_update_name_only(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Topics.UpdateParams = {
            "name": "Monthly Newsletter",
        }
        topic = resend.Topics.update(
            id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e", params=params
        )
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_topics_update_description_only(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Topics.UpdateParams = {
            "description": "Updated description",
        }
        topic = resend.Topics.update(
            id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e", params=params
        )
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_should_update_topics_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Topics.UpdateParams = {
            "name": "Monthly Newsletter",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Topics.update(
                id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e", params=params
            )

    def test_topics_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "topic",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "deleted": True,
            }
        )

        removed: resend.Topics.RemoveTopicResponse = resend.Topics.remove(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        )
        assert removed["object"] == "topic"
        assert removed["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert removed["deleted"] is True

    def test_should_remove_topics_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Topics.remove(id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e")

    def test_topics_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                        "name": "Weekly Newsletter",
                        "description": "Weekly newsletter for our subscribers",
                        "default_subscription": "opt_in",
                        "created_at": "2023-04-08T00:11:13.110779+00:00",
                    }
                ],
            }
        )

        topics: resend.Topics.ListResponse = resend.Topics.list()
        assert topics["object"] == "list"
        assert topics["has_more"] is False
        assert topics["data"][0]["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert topics["data"][0]["name"] == "Weekly Newsletter"
        assert topics["data"][0]["description"] == "Weekly newsletter for our subscribers"
        assert topics["data"][0]["default_subscription"] == "opt_in"

    def test_should_list_topics_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Topics.list()

    def test_topics_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "topic-1",
                        "name": "First Topic",
                        "description": "First topic description",
                        "default_subscription": "opt_in",
                        "created_at": "2023-04-08T00:11:13.110779+00:00",
                    },
                    {
                        "id": "topic-2",
                        "name": "Second Topic",
                        "description": "Second topic description",
                        "default_subscription": "opt_out",
                        "created_at": "2023-04-09T00:11:13.110779+00:00",
                    },
                ],
            }
        )

        params: resend.Topics.ListParams = {
            "limit": 10,
            "after": "previous-topic-id",
        }
        topics: resend.Topics.ListResponse = resend.Topics.list(params=params)
        assert topics["object"] == "list"
        assert topics["has_more"] is True
        assert len(topics["data"]) == 2
        assert topics["data"][0]["id"] == "topic-1"
        assert topics["data"][1]["id"] == "topic-2"

    def test_topics_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "topic-3",
                        "name": "Third Topic",
                        "description": "Third topic description",
                        "default_subscription": "opt_in",
                        "created_at": "2023-04-07T00:11:13.110779+00:00",
                    }
                ],
            }
        )

        params: resend.Topics.ListParams = {
            "limit": 5,
            "before": "later-topic-id",
        }
        topics: resend.Topics.ListResponse = resend.Topics.list(params=params)
        assert topics["object"] == "list"
        assert topics["has_more"] is False
        assert len(topics["data"]) == 1
        assert topics["data"][0]["id"] == "topic-3"
