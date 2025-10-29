from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.pagination_helper import PaginationHelper

from ._contact_property import ContactProperty


class ContactProperties:

    class CreateResponse(TypedDict):
        """
        CreateResponse is the type that wraps the response of the contact property that was created.

        Attributes:
            id (str): The ID of the created contact property
            object (str): The object type, always "contact_property"
        """

        id: str
        """
        The ID of the created contact property.
        """
        object: str
        """
        The object type, always "contact_property".
        """

    class UpdateResponse(TypedDict):
        """
        UpdateResponse is the type that wraps the response of the contact property that was updated.

        Attributes:
            id (str): The ID of the updated contact property
            object (str): The object type, always "contact_property"
        """

        id: str
        """
        The ID of the updated contact property.
        """
        object: str
        """
        The object type, always "contact_property".
        """

    class RemoveResponse(TypedDict):
        """
        RemoveResponse is the type that wraps the response of the contact property that was removed.

        Attributes:
            id (str): The ID of the removed contact property
            object (str): The object type, always "contact_property"
            deleted (bool): Whether the contact property was deleted
        """

        id: str
        """
        The ID of the removed contact property.
        """
        object: str
        """
        The object type, always "contact_property".
        """
        deleted: bool
        """
        Whether the contact property was deleted.
        """

    class ListParams(TypedDict):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            limit (NotRequired[int]): Number of contact properties to retrieve. Maximum is 100, minimum is 1.
            after (NotRequired[str]): The ID after which we'll retrieve more contact properties (for pagination).
            before (NotRequired[str]): The ID before which we'll retrieve more contact properties (for pagination).
        """

        limit: NotRequired[int]
        """
        Number of contact properties to retrieve. Maximum is 100, minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more contact properties (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more contact properties (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of contact property objects with pagination metadata.

        Attributes:
            object (str): The object type, always "list"
            data (List[ContactProperty]): A list of contact property objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list".
        """
        data: List[ContactProperty]
        """
        A list of contact property objects.
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """

    class CreateParams(TypedDict):
        """
        CreateParams is the class that wraps the parameters for creating a contact property.

        Attributes:
            key (str): The key name of the property
            type (str): The data type of the property (e.g., "string", "number", "boolean")
            fallback_value (Any): The default value used when a contact doesn't have this property set
        """

        key: str
        """
        The key name of the property.
        """
        type: str
        """
        The data type of the property (e.g., "string", "number", "boolean").
        """
        fallback_value: Any
        """
        The default value used when a contact doesn't have this property set.
        """

    class UpdateParams(TypedDict):
        """
        UpdateParams is the class that wraps the parameters for updating a contact property.

        Attributes:
            id (str): The contact property ID
            fallback_value (Any): The default value used when a contact doesn't have this property set
        """

        id: str
        """
        The contact property ID.
        """
        fallback_value: Any
        """
        The default value used when a contact doesn't have this property set.
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateResponse:
        """
        Create a new contact property.
        see more: https://resend.com/docs/api-reference/contact-properties/create-contact-property

        Args:
            params (CreateParams): The contact property creation parameters

        Returns:
            CreateResponse: The created contact property response
        """
        path = "/contact-properties"
        resp = request.Request[ContactProperties.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        List all contact properties.
        see more: https://resend.com/docs/api-reference/contact-properties/list-contact-properties

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of contact properties to retrieve (max 100, min 1).
                  If not provided, all contact properties will be returned without pagination.
                - after: ID after which to retrieve more contact properties
                - before: ID before which to retrieve more contact properties

        Returns:
            ListResponse: A list of contact property objects
        """
        base_path = "/contact-properties"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[ContactProperties.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str) -> ContactProperty:
        """
        Get a contact property by ID.
        see more: https://resend.com/docs/api-reference/contact-properties/get-contact-property

        Args:
            id (str): The contact property ID

        Returns:
            ContactProperty: The contact property object
        """
        path = f"/contact-properties/{id}"
        resp = request.Request[ContactProperty](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update an existing contact property.
        see more: https://resend.com/docs/api-reference/contact-properties/update-contact-property

        Args:
            params (UpdateParams): The contact property update parameters

        Returns:
            UpdateResponse: The updated contact property response
        """
        path = f"/contact-properties/{params['id']}"
        resp = request.Request[ContactProperties.UpdateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, id: str) -> RemoveResponse:
        """
        Remove a contact property by ID.
        see more: https://resend.com/docs/api-reference/contact-properties/delete-contact-property

        Args:
            id (str): The contact property ID

        Returns:
            RemoveResponse: The removed contact property response object
        """
        path = f"/contact-properties/{id}"
        resp = request.Request[ContactProperties.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
