from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.emails._received_email import ListReceivedEmail, ReceivedEmail
from resend.pagination_helper import PaginationHelper


class _ListParams(TypedDict):
    limit: NotRequired[int]
    """
    The maximum number of emails to return. Maximum 100, minimum 1.
    """
    after: NotRequired[str]
    """
    Return emails after this cursor for pagination.
    """
    before: NotRequired[str]
    """
    Return emails before this cursor for pagination.
    """


class _ListResponse(TypedDict):
    object: str
    """
    The object type: "list"
    """
    data: List[ListReceivedEmail]
    """
    The list of received email objects.
    """
    has_more: bool
    """
    Whether there are more emails available for pagination.
    """


class Receiving:
    """
    Receiving class that provides methods for retrieving received (inbound) emails.
    """

    class ListParams(_ListParams):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            limit (NotRequired[int]): The maximum number of emails to return. Maximum 100, minimum 1.
            after (NotRequired[str]): Return emails after this cursor for pagination.
            before (NotRequired[str]): Return emails before this cursor for pagination.
        """

    class ListResponse(_ListResponse):
        """
        ListResponse is the type that wraps the response for listing received emails.

        Attributes:
            object (str): The object type: "list"
            data (List[ListReceivedEmail]): The list of received email objects.
            has_more (bool): Whether there are more emails available for pagination.
        """

    @classmethod
    def get(cls, email_id: str) -> ReceivedEmail:
        """
        Retrieve a single received email.
        see more: https://resend.com/docs/api-reference/emails/retrieve-received-email

        Args:
            email_id (str): The ID of the received email to retrieve

        Returns:
            ReceivedEmail: The received email object
        """
        path = f"/emails/receiving/{email_id}"
        resp = request.Request[ReceivedEmail](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of received emails.
        see more: https://resend.com/docs/api-reference/emails/list-received-emails

        Args:
            params (Optional[ListParams]): The list parameters for pagination

        Returns:
            ListResponse: A paginated list of received email objects
        """
        base_path = "/emails/receiving"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Receiving.ListResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp
