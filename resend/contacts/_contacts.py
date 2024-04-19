from typing import Any, Dict, List, cast

from typing_extensions import NotRequired, TypedDict

from resend import request

from ._contact import Contact


class Contacts:
    class CreateParams(TypedDict):
        audience_id: str
        """
        The audience id.
        """
        email: str
        """
        The email of the contact.
        """
        first_name: NotRequired[str]
        """
        The first name of the contact.
        """
        last_name: NotRequired[str]
        """
        The last name of the contact.
        """
        unsubscribed: NotRequired[bool]
        """
        The unsubscribed status of the contact.
        """

    class UpdateParams(TypedDict):
        audience_id: str
        """
        The audience id.
        """
        id: str
        """
        The contact id.
        """
        email: NotRequired[str]
        """
        The email of the contact.
        """
        first_name: NotRequired[str]
        """
        The first name of the contact.
        """
        last_name: NotRequired[str]
        """
        The last name of the contact.
        """
        unsubscribed: NotRequired[bool]
        """
        The unsubscribed status of the contact.
        """

    @classmethod
    def create(cls, params: CreateParams) -> Contact:
        """
        Create a new contact.
        see more: https://resend.com/docs/api-reference/contacts/create-contact
        """
        path = f"/audiences/{params['audience_id']}/contacts"
        return Contact.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params), verb="post"
            ).perform()
        )

    @classmethod
    def update(cls, params: UpdateParams) -> Contact:
        """
        Update an existing contact.
        see more: https://resend.com/docs/api-reference/contacts/update-contact
        """
        path = f"/audiences/{params['audience_id']}/contacts/{params['id']}"
        return Contact.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params), verb="patch"
            ).perform()
        )

    @classmethod
    def list(cls, audience_id: str) -> List[Contact]:
        """
        List all contacts for the provided audience.
        see more: https://resend.com/docs/api-reference/contacts/list-contacts
        """
        path = f"/audiences/{audience_id}/contacts"
        resp = request.Request(path=path, params={}, verb="get").perform()
        return (
            [Contact.new_from_request(contact) for contact in resp["data"]]
            if "data" in resp
            else []
        )

    @classmethod
    def get(cls, id, audience_id: str) -> Contact:
        """
        Get a contact.
        see more: https://resend.com/docs/api-reference/contacts/get-contact
        """
        path = f"/audiences/{audience_id}/contacts/{id}"
        return Contact.new_from_request(
            request.Request(path=path, params={}, verb="get").perform()
        )

    @classmethod
    def remove(cls, audience_id: str, id: str = "", email: str = "") -> Contact:
        """
        Remove a contact by ID or by Email
        see more: https://resend.com/docs/api-reference/contacts/delete-contact
        """
        contact = email if id == "" else id
        if contact == "":
            raise ValueError("id or email must be provided")
        path = f"/audiences/{audience_id}/contacts/{contact}"

        return Contact.new_from_request(
            request.Request(path=path, params={}, verb="delete").perform()
        )
