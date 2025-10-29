import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendContactProperties(ResendBaseTest):
    def test_contact_properties_create(self) -> None:
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
            resend.ContactProperties.create(params)
        )
        assert response["id"] == "prop_123456"
        assert response["object"] == "contact_property"

    def test_should_create_contact_property_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactProperties.CreateParams = {
            "key": "age",
            "type": "number",
            "fallback_value": 0,
        }
        with self.assertRaises(NoContentError):
            _ = resend.ContactProperties.create(params)

    def test_contact_properties_list(self) -> None:
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
            resend.ContactProperties.list()
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert response["data"][0]["id"] == "prop_123456"
        assert response["data"][0]["key"] == "age"
        assert response["data"][0]["type"] == "number"
        assert response["data"][0]["fallback_value"] == 0

    def test_should_list_contact_properties_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.ContactProperties.list()

    def test_contact_properties_list_with_pagination(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "prop_1",
                        "key": "age",
                        "object": "contact_property",
                        "created_at": "2023-10-06T23:47:56.678Z",
                        "type": "number",
                        "fallback_value": 0,
                    },
                    {
                        "id": "prop_2",
                        "key": "city",
                        "object": "contact_property",
                        "created_at": "2023-10-07T23:47:56.678Z",
                        "type": "string",
                        "fallback_value": "Unknown",
                    },
                ],
            }
        )

        params: resend.ContactProperties.ListParams = {
            "limit": 10,
            "after": "prop_0",
        }
        response: resend.ContactProperties.ListResponse = (
            resend.ContactProperties.list(params)
        )
        assert response["object"] == "list"
        assert response["has_more"] is True
        assert len(response["data"]) == 2
        assert response["data"][0]["id"] == "prop_1"
        assert response["data"][1]["id"] == "prop_2"

    def test_contact_properties_get(self) -> None:
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

        property: resend.ContactProperty = resend.ContactProperties.get("prop_123456")
        assert property["id"] == "prop_123456"
        assert property["key"] == "age"
        assert property["type"] == "number"
        assert property["fallback_value"] == 0

    def test_should_get_contact_property_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.ContactProperties.get("prop_123456")

    def test_contact_properties_update(self) -> None:
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
            resend.ContactProperties.update(params)
        )
        assert response["id"] == "prop_123456"
        assert response["object"] == "contact_property"

    def test_should_update_contact_property_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactProperties.UpdateParams = {
            "id": "prop_123456",
            "fallback_value": 18,
        }
        with self.assertRaises(NoContentError):
            _ = resend.ContactProperties.update(params)

    def test_contact_properties_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "contact_property",
                "id": "prop_123456",
                "deleted": True,
            }
        )

        response: resend.ContactProperties.RemoveResponse = (
            resend.ContactProperties.remove("prop_123456")
        )
        assert response["id"] == "prop_123456"
        assert response["object"] == "contact_property"
        assert response["deleted"] is True

    def test_should_remove_contact_property_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.ContactProperties.remove("prop_123456")
