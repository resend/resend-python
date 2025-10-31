from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.pagination_helper import PaginationHelper

from ._contact_segment import ContactSegment


class ContactSegments:
    """
    ContactSegments manages the association between contacts and segments.
    This is separate from the main Contacts API which uses audience_id.
    """

    class AddContactSegmentResponse(TypedDict):
        """
        AddContactSegmentResponse is the type that wraps the response when adding a contact to a segment.

        Attributes:
            id (str): The ID of the contact segment association
        """

        id: str
        """
        The ID of the contact segment association.
        """

    class RemoveContactSegmentResponse(TypedDict):
        """
        RemoveContactSegmentResponse is the type that wraps the response when removing a contact from a segment.

        Attributes:
            id (str): The ID of the contact segment association
            deleted (bool): Whether the association was deleted
        """

        id: str
        """
        The ID of the contact segment association.
        """
        deleted: bool
        """
        Whether the association was deleted.
        """

    class ListContactSegmentsParams(TypedDict):
        """
        ListContactSegmentsParams are the parameters for listing contact segments.

        Attributes:
            limit (NotRequired[int]): Number of segments to retrieve. Maximum is 100, minimum is 1.
            after (NotRequired[str]): The ID after which we'll retrieve more segments (for pagination).
            before (NotRequired[str]): The ID before which we'll retrieve more segments (for pagination).
        """

        limit: NotRequired[int]
        """
        Number of segments to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more segments (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more segments (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListContactSegmentsResponse(TypedDict):
        """
        ListContactSegmentsResponse type that wraps a list of segment objects with pagination metadata.

        Attributes:
            object (str): The object type, always "list"
            data (List[ContactSegment]): A list of segment objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[ContactSegment]
        """
        A list of segment objects.
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """

    class AddParams(TypedDict):
        """
        AddParams for adding a contact to a segment.

        Attributes:
            segment_id (str): The segment ID
            contact_id (NotRequired[str]): The contact ID
            email (NotRequired[str]): The contact email (use either contact_id or email)
        """

        segment_id: str
        """
        The segment ID.
        """
        contact_id: NotRequired[str]
        """
        The contact ID. Either contact_id or email must be provided.
        """
        email: NotRequired[str]
        """
        The contact email. Either contact_id or email must be provided.
        """

    class RemoveParams(TypedDict):
        """
        RemoveParams for removing a contact from a segment.

        Attributes:
            segment_id (str): The segment ID
            contact_id (NotRequired[str]): The contact ID
            email (NotRequired[str]): The contact email (use either contact_id or email)
        """

        segment_id: str
        """
        The segment ID.
        """
        contact_id: NotRequired[str]
        """
        The contact ID. Either contact_id or email must be provided.
        """
        email: NotRequired[str]
        """
        The contact email. Either contact_id or email must be provided.
        """

    class ListParams(TypedDict):
        """
        ListParams for listing segments for a contact.

        Attributes:
            contact_id (NotRequired[str]): The contact ID
            email (NotRequired[str]): The contact email (use either contact_id or email)
        """

        contact_id: NotRequired[str]
        """
        The contact ID. Either contact_id or email must be provided.
        """
        email: NotRequired[str]
        """
        The contact email. Either contact_id or email must be provided.
        """

    @classmethod
    def add(cls, params: AddParams) -> AddContactSegmentResponse:
        """
        Add a contact to a segment.

        Args:
            params (AddParams): Parameters including segment_id and either contact_id or email

        Returns:
            AddContactSegmentResponse: The response containing the association ID

        Raises:
            ValueError: If neither contact_id nor email is provided
        """
        contact_identifier = params.get("email") or params.get("contact_id")
        if not contact_identifier:
            raise ValueError("Either contact_id or email must be provided")

        segment_id = params["segment_id"]
        path = f"/contacts/{contact_identifier}/segments/{segment_id}"
        resp = request.Request[ContactSegments.AddContactSegmentResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, params: RemoveParams) -> RemoveContactSegmentResponse:
        """
        Remove a contact from a segment.

        Args:
            params (RemoveParams): Parameters including segment_id and either contact_id or email

        Returns:
            RemoveContactSegmentResponse: The response containing the deleted status

        Raises:
            ValueError: If neither contact_id nor email is provided
        """
        contact_identifier = params.get("email") or params.get("contact_id")
        if not contact_identifier:
            raise ValueError("Either contact_id or email must be provided")

        segment_id = params["segment_id"]
        path = f"/contacts/{contact_identifier}/segments/{segment_id}"
        resp = request.Request[ContactSegments.RemoveContactSegmentResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    def list(
        cls, params: ListParams, pagination: Optional[ListContactSegmentsParams] = None
    ) -> ListContactSegmentsResponse:
        """
        List all segments for a contact.

        Args:
            params (ListParams): Parameters containing either contact_id or email
            pagination (Optional[ListContactSegmentsParams]): Optional pagination parameters

        Returns:
            ListContactSegmentsResponse: A list of segment objects

        Raises:
            ValueError: If neither contact_id nor email is provided
        """
        contact_identifier = params.get("email") or params.get("contact_id")
        if not contact_identifier:
            raise ValueError("Either contact_id or email must be provided")

        base_path = f"/contacts/{contact_identifier}/segments"
        query_params = cast(Dict[Any, Any], pagination) if pagination else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[ContactSegments.ListContactSegmentsResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp
