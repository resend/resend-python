from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper

from ._contact import Contact
from ._topics import Topics
from .segments._contact_segments import ContactSegments


class Contacts:
    # Sub-API for managing contact-segment associations
    Segments = ContactSegments
    Topics = Topics

    class RemoveContactResponse(BaseResponse):
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

    class ListResponse(BaseResponse):
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

    class CreateContactResponse(BaseResponse):
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

    class UpdateContactResponse(BaseResponse):
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
        email: str
        """
        The email of the contact.
        """
        audience_id: NotRequired[str]
        """
        The audience id. If not provided, creates a global contact.
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
        properties: NotRequired[Dict[str, Any]]
        """
        Custom properties for the contact. Only supported for global contacts (when audience_id is not provided).
        """

    class UpdateParams(TypedDict):
        id: NotRequired[str]
        """
        The contact id. Either id or email must be provided.
        """
        email: NotRequired[str]
        """
        The email of the contact. Either id or email must be provided.
        """
        audience_id: NotRequired[str]
        """
        The audience id. If not provided, updates a global contact.
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
        properties: NotRequired[Dict[str, Any]]
        """
        Custom properties for the contact. Only supported for global contacts (when audience_id is not provided).
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateContactResponse:
        """
        Create a new contact.
        Can create either a global contact or an audience-specific contact.
        see more: https://resend.com/docs/api-reference/contacts/create-contact

        Args:
            params (CreateParams): The contact creation parameters
                - If audience_id is provided: creates audience-specific contact
                - If audience_id is omitted: creates global contact with optional properties field

        Returns:
            CreateContactResponse: The created contact response
        """
        audience_id = params.get("audience_id")

        if audience_id:
            # Audience-specific contact (no properties support)
            path = f"/audiences/{audience_id}/contacts"
        else:
            # Global contact (supports properties)
            path = "/contacts"

        resp = request.Request[Contacts.CreateContactResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateContactResponse:
        """
        Update an existing contact.
        Can update either a global contact or an audience-specific contact.
        see more: https://resend.com/docs/api-reference/contacts/update-contact

        Args:
            params (UpdateParams): The contact update parameters
                - If audience_id is provided: updates audience-specific contact
                - If audience_id is omitted: updates global contact with optional properties field

        Returns:
            UpdateContactResponse: The updated contact response.
        """
        if params.get("id") is None and params.get("email") is None:
            raise ValueError("id or email must be provided")

        # Email takes precedence over id (matching Node.js behavior)
        contact_identifier = (
            params.get("email") if params.get("email") is not None else params.get("id")
        )
        audience_id = params.get("audience_id")

        if audience_id:
            # Audience-specific contact (no properties support)
            path = f"/audiences/{audience_id}/contacts/{contact_identifier}"
        else:
            # Global contact (supports properties)
            path = f"/contacts/{contact_identifier}"

        resp = request.Request[Contacts.UpdateContactResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def list(
        cls, audience_id: Optional[str] = None, params: Optional[ListParams] = None
    ) -> ListResponse:
        """
        List all contacts.
        Can list either global contacts or audience-specific contacts.
        see more: https://resend.com/docs/api-reference/contacts/list-contacts

        Args:
            audience_id (Optional[str]): The audience ID. If not provided, lists all global contacts.
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of contacts to retrieve (max 100, min 1).
                  If not provided, all contacts will be returned without pagination.
                - after: ID after which to retrieve more contacts
                - before: ID before which to retrieve more contacts

        Returns:
            ListResponse: A list of contact objects
        """
        if audience_id:
            # Audience-specific contacts
            base_path = f"/audiences/{audience_id}/contacts"
        else:
            # Global contacts
            base_path = "/contacts"

        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Contacts.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(
        cls,
        audience_id: Optional[str] = None,
        id: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Contact:
        """
        Get a contact.
        Can retrieve either a global contact or an audience-specific contact.
        see more: https://resend.com/docs/api-reference/contacts/get-contact

        Args:
            audience_id (Optional[str]): The audience ID. If not provided, retrieves global contact.
            id (Optional[str]): The contact ID. Either id or email must be provided.
            email (Optional[str]): The contact email. Either id or email must be provided.

        Returns:
            Contact: The contact object
        """
        # Email takes precedence over id (matching Node.js behavior)
        contact_identifier = email if email is not None else id
        if contact_identifier is None:
            raise ValueError("id or email must be provided")

        if audience_id:
            # Audience-specific contact
            path = f"/audiences/{audience_id}/contacts/{contact_identifier}"
        else:
            # Global contact
            path = f"/contacts/{contact_identifier}"

        resp = request.Request[Contact](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(
        cls,
        audience_id: Optional[str] = None,
        id: Optional[str] = None,
        email: Optional[str] = None,
    ) -> RemoveContactResponse:
        """
        Remove a contact by ID or by Email.
        Can remove either a global contact or an audience-specific contact.
        see more: https://resend.com/docs/api-reference/contacts/delete-contact

        Args:
            audience_id (Optional[str]): The audience ID. If not provided, removes global contact.
            id (Optional[str]): The contact ID. Either id or email must be provided.
            email (Optional[str]): The contact email. Either id or email must be provided.

        Returns:
            RemoveContactResponse: The removed contact response object
        """
        # Email takes precedence over id (matching Node.js behavior)
        contact_identifier = email if email is not None else id
        if contact_identifier is None:
            raise ValueError("id or email must be provided")

        if audience_id:
            # Audience-specific contact
            path = f"/audiences/{audience_id}/contacts/{contact_identifier}"
        else:
            # Global contact
            path = f"/contacts/{contact_identifier}"

        resp = request.Request[Contacts.RemoveContactResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
