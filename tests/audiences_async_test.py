import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendAudiencesAsync(ResendBaseTest):
    async def test_audiences_create_async(self) -> None:
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
        audience = await resend.Audiences.create_async(params)
        assert audience["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audience["name"] == "Registered Users"

    async def test_should_create_audiences_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Audiences.CreateParams = {
            "name": "Python SDK Audience",
        }
        with self.assertRaises(NoContentError):
            _ = await resend.Audiences.create_async(params)

    async def test_audiences_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
                "created_at": "2023-10-06T22:59:55.977Z",
            }
        )

        audience = await resend.Audiences.get_async(
            id="78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert audience["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audience["name"] == "Registered Users"
        assert audience["created_at"] == "2023-10-06T22:59:55.977Z"

    async def test_should_get_audiences_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.Audiences.get_async(
                id="78261eea-8f8b-4381-83c6-79fa7120f1cf"
            )

    async def test_audiences_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        rmed = await resend.Audiences.remove_async(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

    async def test_should_remove_audiences_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.Audiences.remove_async(
                id="78261eea-8f8b-4381-83c6-79fa7120f1cf"
            )

    async def test_audiences_list_async(self) -> None:
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

        audiences: resend.Audiences.ListResponse = await resend.Audiences.list_async()
        assert audiences["data"][0]["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audiences["data"][0]["name"] == "Registered Users"

    async def test_should_list_audiences_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.Audiences.list_async()
