from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.emails._attachment import Attachment, RemoteAttachment
from resend.emails._email import Email
from resend.emails._tag import Tag


class _UpdateParams(TypedDict):
    id: str
    """
    The ID of the email to update.
    """
    scheduled_at: NotRequired[str]
    """
    Schedule email to be sent later.
    The date should be in ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
    """


class _UpdateEmailResponse(TypedDict):
    object: str
    """
    The object type: email
    """
    id: str
    """
    The ID of the scheduled email that was canceled.
    """


class _CancelScheduledEmailResponse(TypedDict):
    object: str
    """
    The object type: email
    """
    id: str
    """
    The ID of the scheduled email that was canceled.
    """


# SendParamsFrom is declared with functional TypedDict syntax here because
# "from" is a reserved keyword in Python, and this is the best way to
# support type-checking for it.
_SendParamsFrom = TypedDict(
    "_SendParamsFrom",
    {
        "from": str,
    },
)


class _SendParamsDefault(_SendParamsFrom):
    to: Union[str, List[str]]
    """
    List of email addresses to send the email to.
    """
    subject: str
    """
    The subject of the email.
    """
    bcc: NotRequired[Union[List[str], str]]
    """
    Bcc
    """
    cc: NotRequired[Union[List[str], str]]
    """
    Cc
    """
    reply_to: NotRequired[Union[List[str], str]]
    """
    Reply to
    """
    html: NotRequired[str]
    """
    The HTML content of the email.
    """
    text: NotRequired[str]
    """
    The text content of the email.
    """
    headers: NotRequired[Dict[str, str]]
    """
    Custom headers to be added to the email.
    """
    attachments: NotRequired[List[Union[Attachment, RemoteAttachment]]]
    """
    List of attachments to be added to the email.
    """
    tags: NotRequired[List[Tag]]
    """
    List of tags to be added to the email.
    """
    scheduled_at: NotRequired[str]
    """
    Schedule email to be sent later.
    The date should be in ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
    """


class Emails:

    class CancelScheduledEmailResponse(_CancelScheduledEmailResponse):
        """
        CancelScheduledEmailResponse is the type that wraps the response of the email that was canceled

        Attributes:
            object (str): The object type
            id (str): The ID of the scheduled email that was canceled
        """

    class UpdateEmailResponse(_UpdateEmailResponse):
        """
        UpdateEmailResponse is the type for the updated email response.

        Attributes:
            object (str): The object type
            id (str): The ID of the updated email.
        """

    class UpdateParams(_UpdateParams):
        """
        UpdateParams is the class that wraps the parameters for the update method.

        Attributes:
            id (str): The ID of the email to update.
            scheduled_at (NotRequired[str]): Schedule email to be sent later. \
            The date should be in ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
        """

    class SendParams(_SendParamsDefault):
        """SendParams is the class that wraps the parameters for the send method.

        Attributes:
            from (str): The email address to send the email from.
            to (Union[str, List[str]]): List of email addresses to send the email to.
            subject (str): The subject of the email.
            bcc (NotRequired[Union[List[str], str]]): Bcc
            cc (NotRequired[Union[List[str], str]]): Cc
            reply_to (NotRequired[Union[List[str], str]]): Reply to
            html (NotRequired[str]): The HTML content of the email.
            text (NotRequired[str]): The text content of the email.
            headers (NotRequired[Dict[str, str]]): Custom headers to be added to the email.
            attachments (NotRequired[List[Union[Attachment, RemoteAttachment]]]): List of attachments to be added to the email.
            tags (NotRequired[List[Tag]]): List of tags to be added to the email.
        """

    class SendOptions(TypedDict):
        """
        SendOptions is the class that wraps the options for the send method.

        Attributes:
            idempotency_key (NotRequired[str]): Unique key that ensures the same operation is not processed multiple times.
            Allows for safe retries without duplicating operations.
            If provided, will be sent as the `Idempotency-Key` header.
        """

        idempotency_key: NotRequired[str]
        """
        Unique key that ensures the same operation is not processed multiple times.
        Allows for safe retries without duplicating operations.
        If provided, will be sent as the `Idempotency-Key` header.
        """

    class SendResponse(TypedDict):
        """
        SendResponse is the type that wraps the response of the email that was sent.

        Attributes:
            id (str): The ID of the sent email
        """

        id: str
        """
        The sent Email ID.
        """

    class ListParams(TypedDict):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            limit (NotRequired[int]): The maximum number of emails to return. Defaults to 10, maximum 100.
            after (NotRequired[str]): Return emails after this cursor for pagination.
            before (NotRequired[str]): Return emails before this cursor for pagination.
        """

        limit: NotRequired[int]
        """
        The maximum number of emails to return. Defaults to 10, maximum 100.
        """
        after: NotRequired[str]
        """
        Return emails after this cursor for pagination.
        """
        before: NotRequired[str]
        """
        Return emails before this cursor for pagination.
        """

    class ListResponse(TypedDict):
        """
        ListResponse is the type that wraps the response for listing emails.

        Attributes:
            object (str): The object type: "list"
            data (List[Email]): The list of email objects.
            has_more (bool): Whether there are more emails available for pagination.
        """

        object: str
        """
        The object type: "list"
        """
        data: List[Email]
        """
        The list of email objects.
        """
        has_more: bool
        """
        Whether there are more emails available for pagination.
        """

    @classmethod
    def send(
        cls, params: SendParams, options: Optional[SendOptions] = None
    ) -> SendResponse:
        """
        Send an email through the Resend Email API.
        see more: https://resend.com/docs/api-reference/emails/send-email

        Args:
            params (SendParams): The email parameters
            options (SendOptions): The email options

        Returns:
            id: The ID of the sent email
        """
        path = "/emails"
        resp = request.Request[Email](
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, email_id: str) -> Email:
        """
        Retrieve a single email.
        see more: https://resend.com/docs/api-reference/emails/retrieve-email

        Args:
            email_id (str): The ID of the email to retrieve

        Returns:
            Email: The email object that was retrieved
        """
        path = f"/emails/{email_id}"
        resp = request.Request[Email](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    def cancel(cls, email_id: str) -> CancelScheduledEmailResponse:
        """
        Cancel a scheduled email.
        see more: https://resend.com/docs/api-reference/emails/cancel-email

        Args:
            email_id (str): The ID of the scheduled email to cancel

        Returns:
            CancelScheduledEmailResponse: The response object that contains the ID of the scheduled email that was canceled
        """
        path = f"/emails/{email_id}/cancel"
        resp = request.Request[_CancelScheduledEmailResponse](
            path=path,
            params={},
            verb="post",
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateEmailResponse:
        """
        Update an email.
        see more: https://resend.com/docs/api-reference/emails/update-email

        Args:
            params (UpdateParams): The email parameters to update

        Returns:
            Email: The email object that was updated
        """
        path = f"/emails/{params['id']}"
        resp = request.Request[_UpdateEmailResponse](
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="patch",
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of emails.
        see more: https://resend.com/docs/api-reference/emails/list-emails

        Args:
            params (Optional[ListParams]): The list parameters for pagination

        Returns:
            ListResponse: A paginated list of email objects
        """
        path = "/emails"
        query_params: Dict[str, Union[int, str]] = {}

        if params:
            if "limit" in params:
                query_params["limit"] = params["limit"]
            if "after" in params:
                query_params["after"] = params["after"]
            if "before" in params:
                query_params["before"] = params["before"]

        resp = request.Request[Emails.ListResponse](
            path=path,
            params=query_params,
            verb="get",
        ).perform_with_content()
        return resp
