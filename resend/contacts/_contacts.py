from typing import Any, Dict, List, Optional, cast

from typing_extensions import Literal, NotRequired, TypedDict

from resend import request

from ._contact import Contact, ContactObject, ShortContact


class _ListResponse(TypedDict):
    object: Literal["list"]
    """
    The object type
    """
    data: List[ShortContact]
    """
    A list of contact objects
    """


class _CreateUpdateRemoveResponse(TypedDict):
    object: ContactObject
    """
    The object type
    """
    id: str
    """
    The contact id
    """


class _CreateResponse(_CreateUpdateRemoveResponse):
    pass


class _UpdateResponse(_CreateUpdateRemoveResponse):
    pass


class _RemoveResponse(_CreateUpdateRemoveResponse):
    deleted: bool
    """
    The deleted status of the contact
    """


class Contacts:

    class CreateResponse(_CreateResponse):
        """
        Class that wraps the response of the create contact endpoint

        Attributes:
            object (Literal["contact"]): The object type
            id (str): The contact ID
        """

    class UpdateResponse(_UpdateResponse):
        """
        Class that wraps the response of the update contact endpoint

        Attributes:
            object (Literal["contact"]): The object type
            id (str): The contact ID
        """

    class ListResponse(_ListResponse):
        """
        ListResponse type that wraps a list of contact objects

        Attributes:
            data (List[ShortContact]): A list of contact objects
        """

    class RemoveResponse(_RemoveResponse):
        """
        Class that wraps the response of the remove contact endpoint

        Attributes:
            object (Literal["contact"]): The object type
            id (str): The contact ID
            deleted (bool): The deleted status of the contact
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
    def create(cls, params: CreateParams) -> CreateResponse:
        """
        Create a new contact.
        see more: https://resend.com/docs/api-reference/contacts/create-contact

        Args:
            params (CreateParams): The contact creation parameters

        Returns:
            Contact: The new contact object
        """
        path = f"/audiences/{params['audience_id']}/contacts"
        resp = request.Request[_CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
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
        resp = request.Request[_UpdateResponse](
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
    def get(
        cls, audience_id: str, id: Optional[str] = None, email: Optional[str] = None
    ) -> Contact:
        """
        Get a contact.
        see more: https://resend.com/docs/api-reference/contacts/get-contact

        Args:
            id (str): The contact ID
            audience_id (str): The audience ID
            email (Optional[str]): The contact email

        Returns:
            Contact: The contact object
        """
        contact = email if id is None else id
        if contact is None:
            raise ValueError("id or email must be provided")

        path = f"/audiences/{audience_id}/contacts/{contact}"
        resp = request.Request[Contact](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(
        cls, audience_id: str, id: Optional[str] = None, email: Optional[str] = None
    ) -> RemoveResponse:
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
        contact = email if id is None else id
        if contact is None:
            raise ValueError("id or email must be provided")
        path = f"/audiences/{audience_id}/contacts/{contact}"

        resp = request.Request[_RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
