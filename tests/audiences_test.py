import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendAudiences(ResendBaseTest):
    def test_audiences_create(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
            }
        )

        params: resend.Audiences.CreateParams = {
            "name": "Python SDK Audience",
        }
        audience = resend.Audiences.create(params)
        assert audience["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audience["name"] == "Registered Users"

    def test_should_create_audiences_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Audiences.CreateParams = {
            "name": "Python SDK Audience",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Audiences.create(params)

    def test_audiences_get(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
                "created_at": "2023-10-06T22:59:55.977Z",
            }
        )

        audience = resend.Audiences.get(id="78261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert audience["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audience["name"] == "Registered Users"
        assert audience["created_at"] == "2023-10-06T22:59:55.977Z"

    def test_should_get_audiences_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Audiences.get(id="78261eea-8f8b-4381-83c6-79fa7120f1cf")

    def test_audiences_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        rmed: resend.Audiences.RemoveAudienceResponse = resend.Audiences.remove(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert rmed["object"] == "audience"
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

    def test_should_remove_audiences_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Audiences.remove(id="78261eea-8f8b-4381-83c6-79fa7120f1cf")

    def test_audiences_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "name": "Registered Users",
                        "created_at": "2023-10-06T22:59:55.977Z",
                    }
                ],
            }
        )

        audiences: resend.Audiences.ListResponse = resend.Audiences.list()
        assert audiences["object"] == "list"
        assert audiences["has_more"] is False
        assert audiences["data"][0]["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audiences["data"][0]["name"] == "Registered Users"

    def test_should_list_audiences_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Audiences.list()

    def test_audiences_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "audience-1",
                        "name": "First Audience",
                        "created_at": "2023-10-06T22:59:55.977Z",
                    },
                    {
                        "id": "audience-2",
                        "name": "Second Audience",
                        "created_at": "2023-10-07T22:59:55.977Z",
                    }
                ],
            }
        )

        params: resend.Audiences.ListParams = {
            "limit": 10,
            "after": "previous-audience-id"
        }
        audiences: resend.Audiences.ListResponse = resend.Audiences.list(params=params)
        assert audiences["object"] == "list"
        assert audiences["has_more"] is True
        assert len(audiences["data"]) == 2
        assert audiences["data"][0]["id"] == "audience-1"
        assert audiences["data"][1]["id"] == "audience-2"

    def test_audiences_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "audience-3",
                        "name": "Third Audience",
                        "created_at": "2023-10-05T22:59:55.977Z",
                    }
                ],
            }
        )

        params: resend.Audiences.ListParams = {
            "limit": 5,
            "before": "later-audience-id"
        }
        audiences: resend.Audiences.ListResponse = resend.Audiences.list(params=params)
        assert audiences["object"] == "list"
        assert audiences["has_more"] is False
        assert len(audiences["data"]) == 1
        assert audiences["data"][0]["id"] == "audience-3"
