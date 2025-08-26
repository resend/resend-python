from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request

from ._contact import Contact

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class Contacts:

    class RemoveContactResponse(TypedDict):
        """
        RemoveContactResponse is the type that wraps the response of the contact that was removed

        Attributes:
            object (str): 'contact'
            contact (str): The ID of the removed contact
            deleted (bool): Whether the contact was deleted
        """

        object: str
        """
        The object type: contact
        """
        contact: str
        """
        The ID of the removed contact.
        """
        deleted: bool
        """
        Whether the contact was deleted.
        """

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of contact objects

        Attributes:
            object (str): The object type: list
            data (List[Contact]): A list of contact objects
        """

        object: str
        """
        The object type: list
        """
        data: List[Contact]
        """
        A list of contact objects
        """

    class CreateContactResponse(TypedDict):
        """
        CreateContactResponse is the type that wraps the response of the contact that was created

        Attributes:
            object (str): The ID of the created contact
            id (str): The ID of the created contact
        """

        object: str
        """
        The object type: email
        """
        id: str
        """
        The ID of the scheduled email that was canceled.
        """

    class UpdateContactResponse(TypedDict):
        """
        UpdateContactResponse is the type that wraps the response of the contact that was updated

        Attributes:
            object (str): The ID of the updated contact
            id (str): The ID of the updated contact
        """

        object: str
        """
        The object type: email
        """
        id: str
        """
        The ID of the updated contact.
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
    def create(cls, params: CreateParams) -> CreateContactResponse:
        """
        Create a new contact.
        see more: https://resend.com/docs/api-reference/contacts/create-contact

        Args:
            params (CreateParams): The contact creation parameters

        Returns:
            CreateContactResponse: The created contact response
        """

        path = f"/audiences/{params['audience_id']}/contacts"
        resp = request.Request[Contacts.CreateContactResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateContactResponse:
        """
        Update an existing contact.
        see more: https://resend.com/docs/api-reference/contacts/update-contact

        Args:
            params (UpdateParams): The contact update parameters

        Returns:
            UpdateContactResponse: The updated contact response.
        """
        if params.get("id") is None and params.get("email") is None:
            raise ValueError("id or email must be provided")

        val = params.get("id") if params.get("id") is not None else params.get("email")

        path = f"/audiences/{params['audience_id']}/contacts/{val}"
        resp = request.Request[Contacts.UpdateContactResponse](
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
        resp = request.Request[Contacts.ListResponse](
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
    ) -> RemoveContactResponse:
        """
        Remove a contact by ID or by Email
        see more: https://resend.com/docs/api-reference/contacts/delete-contact

        Args:
            audience_id (str): The audience ID
            id (str): The contact ID
            email (str): The contact email

        Returns:
            RemoveContactResponse: The removed contact response object
        """
        contact = email if id is None else id
        if contact is None:
            raise ValueError("id or email must be provided")
        path = f"/audiences/{audience_id}/contacts/{contact}"

        resp = request.Request[Contacts.RemoveContactResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(cls, params: CreateParams) -> Contact:
        """
        Create a new contact (async).
        see more: https://resend.com/docs/api-reference/contacts/create-contact

        Args:
            params (CreateParams): The contact creation parameters

        Returns:
            Contact: The new contact object
        """
        path = f"/audiences/{params['audience_id']}/contacts"
        resp = await AsyncRequest[Contact](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> Contact:
        """
        Update an existing contact (async).
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
        resp = await AsyncRequest[Contact](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, audience_id: str) -> ListResponse:
        """
        List all contacts for the provided audience (async).
        see more: https://resend.com/docs/api-reference/contacts/list-contacts

        Args:
            audience_id (str): The audience ID

        Returns:
            ListResponse: A list of contact objects
        """
        path = f"/audiences/{audience_id}/contacts"
        resp = await AsyncRequest[_ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(
        cls, audience_id: str, id: Optional[str] = None, email: Optional[str] = None
    ) -> Contact:
        """
        Get a contact (async).
        see more: https://resend.com/docs/api-reference/contacts/get-contact

        Args:
            audience_id (str): The audience ID
            id (Optional[str]): The contact ID
            email (Optional[str]): The contact email

        Returns:
            Contact: The contact object
        """
        contact = email if id is None else id
        if contact is None:
            raise ValueError("id or email must be provided")

        path = f"/audiences/{audience_id}/contacts/{contact}"
        resp = await AsyncRequest[Contact](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(
        cls, audience_id: str, id: Optional[str] = None, email: Optional[str] = None
    ) -> Contact:
        """
        Remove a contact by ID or by Email (async).
        see more: https://resend.com/docs/api-reference/contacts/delete-contact

        Args:
            audience_id (str): The audience ID
            id (Optional[str]): The contact ID
            email (Optional[str]): The contact email

        Returns:
            Contact: The removed contact object
        """
        contact = email if id is None else id
        if contact is None:
            raise ValueError("id or email must be provided")
        path = f"/audiences/{audience_id}/contacts/{contact}"

        resp = await AsyncRequest[Contact](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
