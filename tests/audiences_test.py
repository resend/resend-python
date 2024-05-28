import resend
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

    def test_audiences_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        rmed = resend.Audiences.remove("78261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

    def test_audiences_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
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
        assert audiences["data"][0]["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audiences["data"][0]["name"] == "Registered Users"
