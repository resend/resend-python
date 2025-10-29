from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.pagination_helper import PaginationHelper

from ._contact_topic import ContactTopic, TopicSubscriptionUpdate


class _ListParams(TypedDict):
    limit: NotRequired[int]
    """
    Number of topics to retrieve. Maximum is 100, minimum is 1.
    """
    after: NotRequired[str]
    """
    The ID after which we'll retrieve more topics (for pagination).
    """
    before: NotRequired[str]
    """
    The ID before which we'll retrieve more topics (for pagination).
    """


class _ListResponse(TypedDict):
    object: str
    """
    The object type: "list"
    """
    data: List[ContactTopic]
    """
    The list of contact topic objects.
    """
    has_more: bool
    """
    Whether there are more topics available for pagination.
    """


class _UpdateParams(TypedDict):
    id: NotRequired[str]
    """
    The contact ID.
    """
    email: NotRequired[str]
    """
    The contact email.
    """
    topics: List[TopicSubscriptionUpdate]
    """
    List of topic subscription updates.
    """


class _UpdateResponse(TypedDict):
    id: str
    """
    The contact ID.
    """
    object: str
    """
    The object type: "contact"
    """


class Topics:
    """
    Topics class that provides methods for managing contact topic subscriptions.
    """

    class ListParams(_ListParams):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            limit (NotRequired[int]): Number of topics to retrieve. Maximum is 100, minimum is 1.
            after (NotRequired[str]): Return topics after this cursor for pagination.
            before (NotRequired[str]): Return topics before this cursor for pagination.
        """

    class ListResponse(_ListResponse):
        """
        ListResponse is the type that wraps the response for listing contact topics.

        Attributes:
            object (str): The object type: "list"
            data (List[ContactTopic]): The list of contact topic objects.
            has_more (bool): Whether there are more topics available for pagination.
        """

    class UpdateParams(_UpdateParams):
        """
        UpdateParams is the class that wraps the parameters for updating contact topic subscriptions.

        Attributes:
            id (NotRequired[str]): The contact ID (either id or email must be provided)
            email (NotRequired[str]): The contact email (either id or email must be provided)
            topics (List[TopicSubscriptionUpdate]): List of topic subscription updates
        """

    class UpdateResponse(_UpdateResponse):
        """
        UpdateResponse is the type that wraps the response for updating contact topics.

        Attributes:
            id (str): The contact ID
            object (str): The object type: "contact"
        """

    @classmethod
    def list(
        cls,
        contact_id: Optional[str] = None,
        email: Optional[str] = None,
        params: Optional["Topics.ListParams"] = None,
    ) -> "Topics.ListResponse":
        """
        List all topics for a contact.
        see more: https://resend.com/docs/api-reference/contacts/list-contact-topics

        Args:
            contact_id (Optional[str]): The contact ID (either contact_id or email must be provided)
            email (Optional[str]): The contact email (either contact_id or email must be provided)
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of topics to retrieve (max 100, min 1).
                  If not provided, all topics will be returned without pagination.
                - after: ID after which to retrieve more topics
                - before: ID before which to retrieve more topics

        Returns:
            ListResponse: A list of contact topic objects

        Raises:
            ValueError: If neither contact_id nor email is provided
        """
        contact = email if contact_id is None else contact_id
        if contact is None:
            raise ValueError("contact_id or email must be provided")

        base_path = f"/contacts/{contact}/topics"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[_ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update topic subscriptions for a contact.
        see more: https://resend.com/docs/api-reference/contacts/update-contact-topics

        Args:
            params (UpdateParams): The topic update parameters
                - id: The contact ID (either id or email must be provided)
                - email: The contact email (either id or email must be provided)
                - topics: List of topic subscription updates

        Returns:
            UpdateResponse: The updated contact response

        Raises:
            ValueError: If neither id nor email is provided in params
        """
        if params.get("id") is None and params.get("email") is None:
            raise ValueError("id or email must be provided")

        contact = params.get("id") if params.get("id") is not None else params.get("email")
        path = f"/contacts/{contact}/topics"

        # Send the topics array directly as the request body (not wrapped in an object)
        # The Request class accepts Union[Dict, List] as params
        request_body: Union[Dict[str, Any], List[Dict[str, Any]]] = cast(
            List[Dict[str, Any]], params["topics"]
        )

        resp = request.Request[_UpdateResponse](
            path=path, params=request_body, verb="patch"
        ).perform_with_content()
        return resp
