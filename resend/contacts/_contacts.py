from typing import Any, Dict, List, cast

from typing_extensions import NotRequired, TypedDict

from resend import request

from ._contact import Contact


class _ListResponse(TypedDict):
    data: List[Contact]
    """
    A list of contact objects
    """


class Contacts:

    class ListResponse(_ListResponse):
        """
        ListResponse type that wraps a list of contact objects

        Attributes:
            data (List[Contact]): A list of contact objects
        """

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
        id: NotRequired[str]
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

        Args:
            params (CreateParams): The contact creation parameters

        Returns:
            Contact: The new contact object
        """
        path = f"/audiences/{params['audience_id']}/contacts"
        resp = request.Request[Contact](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> Contact:
        """
        Update an existing contact.
        see more: https://resend.com/docs/api-reference/contacts/update-contact

        Args:
            params (UpdateParams): The contact update parameters

        Returns:
            Contact: The updated contact object
        """
        if params.get("id") is None and params.get("email") is None:
            raise ValueError("id or email must be provided")

        val = params.get("id") if params.get("id") is not None else params.get("email")

        path = f"/audiences/{params['audience_id']}/contacts/{val}"
        resp = request.Request[Contact](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, audience_id: str) -> ListResponse:
        """
        List all contacts for the provided audience.
        see more: https://resend.com/docs/api-reference/contacts/list-contacts

        Args:
            audience_id (str): The audience ID

        Returns:
            ListResponse: A list of contact objects
        """
        path = f"/audiences/{audience_id}/contacts"
        resp = request.Request[_ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str, audience_id: str) -> Contact:
        """
        Get a contact.
        see more: https://resend.com/docs/api-reference/contacts/get-contact

        Args:
            id (str): The contact ID
            audience_id (str): The audience ID

        Returns:
            Contact: The contact object
        """
        path = f"/audiences/{audience_id}/contacts/{id}"
        resp = request.Request[Contact](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, audience_id: str, id: str = "", email: str = "") -> Contact:
        """
        Remove a contact by ID or by Email
        see more: https://resend.com/docs/api-reference/contacts/delete-contact

        Args:
            audience_id (str): The audience ID
            id (str): The contact ID
            email (str): The contact email

        Returns:
            Contact: The removed contact object
        """
        contact = email if id == "" else id
        if contact == "":
            raise ValueError("id or email must be provided")
        path = f"/audiences/{audience_id}/contacts/{contact}"

        resp = request.Request[Contact](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
