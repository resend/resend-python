import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendContactPropertiesAsync(ResendBaseTest):
    async def test_contact_properties_create_async(self) -> None:
        self.set_mock_json(
            {
                "object": "contact_property",
                "id": "prop_123456",
            }
        )

        params: resend.ContactProperties.CreateParams = {
            "key": "age",
            "type": "number",
            "fallback_value": 0,
        }
        response: resend.ContactProperties.CreateResponse = (
            await resend.ContactProperties.create_async(params)
        )
        assert response["id"] == "prop_123456"
        assert response["object"] == "contact_property"

    async def test_should_create_contact_property_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactProperties.CreateParams = {
            "key": "age",
            "type": "number",
            "fallback_value": 0,
        }
        with self.assertRaises(NoContentError):
            _ = await resend.ContactProperties.create_async(params)

    async def test_contact_properties_get_async(self) -> None:
        self.set_mock_json(
            {
                "id": "prop_123456",
                "key": "age",
                "object": "contact_property",
                "created_at": "2023-10-06T23:47:56.678Z",
                "type": "number",
                "fallback_value": 0,
            }
        )

        prop: resend.ContactProperty = await resend.ContactProperties.get_async(
            "prop_123456"
        )
        assert prop["id"] == "prop_123456"
        assert prop["key"] == "age"
        assert prop["type"] == "number"
        assert prop["fallback_value"] == 0

    async def test_should_get_contact_property_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.ContactProperties.get_async("prop_123456")

    async def test_contact_properties_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "prop_123456",
                        "key": "age",
                        "object": "contact_property",
                        "created_at": "2023-10-06T23:47:56.678Z",
                        "type": "number",
                        "fallback_value": 0,
                    }
                ],
            }
        )

        response: resend.ContactProperties.ListResponse = (
            await resend.ContactProperties.list_async()
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert response["data"][0]["id"] == "prop_123456"

    async def test_should_list_contact_properties_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.ContactProperties.list_async()

    async def test_contact_properties_update_async(self) -> None:
        self.set_mock_json(
            {
                "object": "contact_property",
                "id": "prop_123456",
            }
        )

        params: resend.ContactProperties.UpdateParams = {
            "id": "prop_123456",
            "fallback_value": 18,
        }
        response: resend.ContactProperties.UpdateResponse = (
            await resend.ContactProperties.update_async(params)
        )
        assert response["id"] == "prop_123456"
        assert response["object"] == "contact_property"

    async def test_should_update_contact_property_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactProperties.UpdateParams = {
            "id": "prop_123456",
            "fallback_value": 18,
        }
        with self.assertRaises(NoContentError):
            _ = await resend.ContactProperties.update_async(params)

    async def test_contact_properties_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "contact_property",
                "id": "prop_123456",
                "deleted": True,
            }
        )

        response: resend.ContactProperties.RemoveResponse = (
            await resend.ContactProperties.remove_async("prop_123456")
        )
        assert response["id"] == "prop_123456"
        assert response["object"] == "contact_property"
        assert response["deleted"] is True

    async def test_should_remove_contact_property_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = await resend.ContactProperties.remove_async("prop_123456")
