import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendContacts(ResendBaseTest):
    def test_contacts_create(self) -> None:
        self.set_mock_json(
            {"object": "contact", "id": "479e3145-dd38-476b-932c-529ceb705947"}
        )

        params: resend.Contacts.CreateParams = {
            "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            "email": "steve.wozniak@gmail.com",
            "first_name": "Steve",
            "last_name": "Wozniak",
            "unsubscribed": True,
        }
        contact: resend.Contacts.CreateContactResponse = resend.Contacts.create(params)
        assert contact["id"] == "479e3145-dd38-476b-932c-529ceb705947"

    def test_should_create_contacts_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Contacts.CreateParams = {
            "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            "email": "steve.wozniak@gmail.com",
            "first_name": "Steve",
            "last_name": "Wozniak",
            "unsubscribed": True,
        }
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.create(params)

    def test_contacts_update(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "id": "479e3145-dd38-476b-932c-529ceb705947",
            }
        )

        params: resend.Contacts.UpdateParams = {
            "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            "id": "479e3145-dd38-476b-932c-529ceb705947",
            "first_name": "Updated",
            "unsubscribed": True,
        }
        contact = resend.Contacts.update(params)
        assert contact["id"] == "479e3145-dd38-476b-932c-529ceb705947"

    def test_contacts_update_missing_required_params(self) -> None:

        params: resend.Contacts.UpdateParams = {
            "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            "first_name": "Updated",
            "unsubscribed": True,
        }

        try:
            resend.Contacts.update(params)
        except ValueError as e:
            assert str(e) == "id or email must be provided"

    def test_should_update_contacts_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Contacts.UpdateParams = {
            "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            "id": "479e3145-dd38-476b-932c-529ceb705947",
            "first_name": "Updated",
            "unsubscribed": True,
        }
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.update(params)

    def test_contacts_get(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "email": "steve.wozniak@gmail.com",
                "first_name": "Steve",
                "last_name": "Wozniak",
                "created_at": "2023-10-06T23:47:56.678Z",
                "unsubscribed": False,
            }
        )

        contact: resend.Contact = resend.Contacts.get(
            id="e169aa45-1ecf-4183-9955-b1499d5701d3",
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
        )
        assert contact["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert contact["email"] == "steve.wozniak@gmail.com"
        assert contact.get("first_name") == "Steve"
        assert contact.get("last_name") == "Wozniak"
        assert contact["created_at"] == "2023-10-06T23:47:56.678Z"
        assert contact["unsubscribed"] is False

    def test_contacts_get_by_email(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "email": "steve@woz.com",
                "first_name": "Steve",
                "last_name": "Wozniak",
                "created_at": "2023-10-06T23:47:56.678Z",
                "unsubscribed": False,
            }
        )

        contact: resend.Contact = resend.Contacts.get(
            email="steve@woz.com",
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
        )
        assert contact["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert contact["email"] == "steve@woz.com"
        assert contact["first_name"] == "Steve"
        assert contact["last_name"] == "Wozniak"
        assert contact["created_at"] == "2023-10-06T23:47:56.678Z"
        assert contact["unsubscribed"] is False

    def test_contacts_get_raises(self) -> None:
        resend.api_key = "re_123"

        with self.assertRaises(ValueError) as context:
            resend.Contacts.get(
                audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            )

        self.assertEqual("id or email must be provided", str(context.exception))

    def test_should_get_contacts_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.get(
                id="e169aa45-1ecf-4183-9955-b1499d5701d3",
                audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            )

    def test_contacts_remove_by_id(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "contact": "520784e2-887d-4c25-b53c-4ad46ad38100",
                "deleted": True,
            }
        )

        rmed = resend.Contacts.remove(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            id="78261eea-8f8b-4381-83c6-79fa7120f1cf",
        )
        assert rmed["contact"] == "520784e2-887d-4c25-b53c-4ad46ad38100"
        assert rmed["deleted"] is True

    def test_should_remove_contacts_by_id_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.remove(
                audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
                id="78261eea-8f8b-4381-83c6-79fa7120f1cf",
            )

    def test_contacts_remove_by_email(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "contact": "520784e2-887d-4c25-b53c-4ad46ad38100",
                "deleted": True,
            }
        )

        rmed: resend.Contacts.RemoveContactResponse = resend.Contacts.remove(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            email="someemail@email.com",
        )
        assert rmed["contact"] == "520784e2-887d-4c25-b53c-4ad46ad38100"
        assert rmed["deleted"] is True

    def test_should_remove_contacts_by_email_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.remove(
                audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
                email="someemail@email.com",
            )

    def test_contacts_remove_raises(self) -> None:
        resend.api_key = "re_123"

        with self.assertRaises(ValueError) as context:
            resend.Contacts.remove(
                audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
            )

        self.assertEqual("id or email must be provided", str(context.exception))

    def test_contacts_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "email": "steve.wozniak@gmail.com",
                        "first_name": "Steve",
                        "last_name": "Wozniak",
                        "created_at": "2023-10-06T23:47:56.678Z",
                        "unsubscribed": False,
                    }
                ],
            }
        )

        contacts: resend.Contacts.ListResponse = resend.Contacts.list(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8"
        )
        assert contacts["object"] == "list"
        assert contacts["has_more"] is False
        assert contacts["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert contacts["data"][0]["email"] == "steve.wozniak@gmail.com"
        assert contacts["data"][0].get("first_name") == "Steve"
        assert contacts["data"][0].get("last_name") == "Wozniak"
        assert contacts["data"][0]["created_at"] == "2023-10-06T23:47:56.678Z"
        assert contacts["data"][0]["unsubscribed"] is False

    def test_should_list_contacts_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.list(audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8")

    def test_contacts_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "contact-1",
                        "email": "contact1@example.com",
                        "first_name": "Contact",
                        "last_name": "One",
                        "created_at": "2023-10-06T23:47:56.678Z",
                        "unsubscribed": False,
                    },
                    {
                        "id": "contact-2",
                        "email": "contact2@example.com",
                        "first_name": "Contact",
                        "last_name": "Two",
                        "created_at": "2023-10-07T23:47:56.678Z",
                        "unsubscribed": False,
                    },
                ],
            }
        )

        params: resend.Contacts.ListParams = {
            "limit": 10,
            "after": "previous-contact-id",
        }
        contacts: resend.Contacts.ListResponse = resend.Contacts.list(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8", params=params
        )
        assert contacts["object"] == "list"
        assert contacts["has_more"] is True
        assert len(contacts["data"]) == 2
        assert contacts["data"][0]["id"] == "contact-1"
        assert contacts["data"][1]["id"] == "contact-2"

    def test_contacts_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "contact-3",
                        "email": "contact3@example.com",
                        "first_name": "Contact",
                        "last_name": "Three",
                        "created_at": "2023-10-05T23:47:56.678Z",
                        "unsubscribed": False,
                    }
                ],
            }
        )

        params: resend.Contacts.ListParams = {"limit": 5, "before": "later-contact-id"}
        contacts: resend.Contacts.ListResponse = resend.Contacts.list(
            audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8", params=params
        )
        assert contacts["object"] == "list"
        assert contacts["has_more"] is False
        assert len(contacts["data"]) == 1
        assert contacts["data"][0]["id"] == "contact-3"

    # Global contacts tests (without audience_id)
    def test_contacts_create_global(self) -> None:
        self.set_mock_json({"object": "contact", "id": "global-contact-123"})

        params: resend.Contacts.CreateParams = {
            "email": "global@example.com",
            "first_name": "Global",
            "last_name": "Contact",
            "properties": {"tier": "premium", "role": "admin"},
        }
        contact: resend.Contacts.CreateContactResponse = resend.Contacts.create(params)
        assert contact["id"] == "global-contact-123"

    def test_contacts_update_global(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "id": "global-contact-123",
            }
        )

        params: resend.Contacts.UpdateParams = {
            "id": "global-contact-123",
            "first_name": "Updated Global",
            "properties": {"tier": "enterprise"},
        }
        contact = resend.Contacts.update(params)
        assert contact["id"] == "global-contact-123"

    def test_contacts_get_global(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "id": "global-contact-123",
                "email": "global@example.com",
                "first_name": "Global",
                "last_name": "Contact",
                "created_at": "2023-10-06T23:47:56.678Z",
                "unsubscribed": False,
                "properties": {"tier": "premium"},
            }
        )

        contact: resend.Contact = resend.Contacts.get(id="global-contact-123")
        assert contact["id"] == "global-contact-123"
        assert contact["email"] == "global@example.com"
        assert contact.get("properties") == {"tier": "premium"}

    # Note: Global contacts only accept UUID identifiers, not emails
    # The API returns "The `id` must be a valid UUID" for email identifiers

    def test_contacts_list_global(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "global-1",
                        "email": "global1@example.com",
                        "first_name": "Global",
                        "last_name": "One",
                        "created_at": "2023-10-06T23:47:56.678Z",
                        "unsubscribed": False,
                        "properties": {"tier": "free"},
                    },
                    {
                        "id": "global-2",
                        "email": "global2@example.com",
                        "first_name": "Global",
                        "last_name": "Two",
                        "created_at": "2023-10-07T23:47:56.678Z",
                        "unsubscribed": False,
                        "properties": {"tier": "premium"},
                    },
                ],
            }
        )

        contacts: resend.Contacts.ListResponse = resend.Contacts.list()
        assert contacts["object"] == "list"
        assert contacts["has_more"] is False
        assert len(contacts["data"]) == 2
        assert contacts["data"][0]["id"] == "global-1"
        assert contacts["data"][1]["id"] == "global-2"

    def test_contacts_remove_global_by_id(self) -> None:
        self.set_mock_json(
            {
                "object": "contact",
                "contact": "global-contact-789",
                "deleted": True,
            }
        )

        rmed = resend.Contacts.remove(id="global-contact-789")
        assert rmed["contact"] == "global-contact-789"
        assert rmed["deleted"] is True

    # Note: Global contacts only accept UUID identifiers for remove operations
    # Email-based removal would fail with "The `id` must be a valid UUID" error
