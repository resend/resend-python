from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.pagination_helper import PaginationHelper

from ._contact import Contact
from .segments._contact_segments import ContactSegments


class Contacts:
    # Sub-API for managing contact-segment associations
    Segments = ContactSegments

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

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of contacts to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more contacts (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more contacts (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of contact objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[Contact]): A list of contact objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[Contact]
        """
        A list of contact objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
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
    def list(
        cls, audience_id: str, params: Optional[ListParams] = None
    ) -> ListResponse:
        """
        List all contacts for the provided audience.
        see more: https://resend.com/docs/api-reference/contacts/list-contacts

        Args:
            audience_id (str): The audience ID
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of contacts to retrieve (max 100, min 1).
                  If not provided, all contacts will be returned without pagination.
                - after: ID after which to retrieve more contacts
                - before: ID before which to retrieve more contacts

        Returns:
            ListResponse: A list of contact objects
        """
        base_path = f"/audiences/{audience_id}/contacts"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
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
