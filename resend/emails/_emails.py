from typing import Any, Dict, List, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.emails._attachment import Attachment
from resend.emails._email import Email
from resend.emails._tag import Tag

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
    attachments: NotRequired[List[Attachment]]
    """
    List of attachments to be added to the email.
    """
    tags: NotRequired[List[Tag]]
    """
    List of tags to be added to the email.
    """


class Emails:
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
            attachments (NotRequired[List[Attachment]]): List of attachments to be added to the email.
            tags (NotRequired[List[Tag]]): List of tags to be added to the email.
        """

    @classmethod
    def send(cls, params: SendParams) -> Email:
        """
        Send an email through the Resend Email API.
        see more: https://resend.com/docs/api-reference/emails/send-email

        Args:
            params (SendParams): The email parameters

        Returns:
            Email: The email object that was sent
        """
        path = "/emails"
        resp = request.Request[Email](
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
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
