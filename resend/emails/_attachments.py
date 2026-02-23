from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.emails._received_email import (EmailAttachment,
                                           EmailAttachmentDetails)
from resend.pagination_helper import PaginationHelper


class _ListParams(TypedDict):
    limit: NotRequired[int]
    """
    The maximum number of attachments to return. Maximum 100, minimum 1.
    """
    after: NotRequired[str]
    """
    Return attachments after this cursor for pagination.
    """
    before: NotRequired[str]
    """
    Return attachments before this cursor for pagination.
    """


class _ListResponse(BaseResponse):
    object: str
    """
    The object type: "list"
    """
    data: List[EmailAttachment]
    """
    The list of attachment objects.
    """
    has_more: bool
    """
    Whether there are more attachments available for pagination.
    """


class Attachments:
    """
    Attachments class that provides methods for retrieving attachments from sent emails.
    """

    class ListParams(_ListParams):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            limit (NotRequired[int]): The maximum number of attachments to return. Maximum 100, minimum 1.
            after (NotRequired[str]): Return attachments after this cursor for pagination.
            before (NotRequired[str]): Return attachments before this cursor for pagination.
        """

    class ListResponse(_ListResponse):
        """
        ListResponse is the type that wraps the response for listing attachments.

        Attributes:
            object (str): The object type: "list"
            data (List[EmailAttachment]): The list of attachment objects.
            has_more (bool): Whether there are more attachments available for pagination.
        """

    @classmethod
    def get(cls, email_id: str, attachment_id: str) -> EmailAttachmentDetails:
        """
        Retrieve a single attachment from a sent email.
        see more: https://resend.com/docs/api-reference/attachments/retrieve-sent-email-attachment

        Args:
            email_id (str): The ID of the sent email
            attachment_id (str): The ID of the attachment to retrieve

        Returns:
            EmailAttachmentDetails: The attachment details including download URL
        """
        path = f"/emails/{email_id}/attachments/{attachment_id}"
        resp = request.Request[EmailAttachmentDetails](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, email_id: str, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of attachments from a sent email.
        see more: https://resend.com/docs/api-reference/attachments/list-sent-email-attachments

        Args:
            email_id (str): The ID of the sent email
            params (Optional[ListParams]): The list parameters for pagination

        Returns:
            ListResponse: A paginated list of attachment objects
        """
        base_path = f"/emails/{email_id}/attachments"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Attachments.ListResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp
