from typing import Any, Dict, List, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.emails._attachment import Attachment
from resend.emails._email import Email
from resend.emails._tag import Tag
from resend.utils import replace_params


class SendParamsDefault(TypedDict):
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


class SendParamsFrom_(SendParamsDefault):
    from_: str
    """
    The email address of the sender.
    "from" is a reserved keyword in python.
    So we accept either "from_" or "sender"
    """


class SendParamsSender(SendParamsDefault):
    sender: str
    """
    The email address of the sender.
    "from" is a reserved keyword in python.
    So we accept either "from_" or "sender"
    """


class Emails:
    SendParams = Union[SendParamsFrom_, SendParamsSender]

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

        # replace "from_" or "sender" with "from"
        p = replace_params(cast(Dict[Any, Any], params))

        return Email.new_from_request(
            request.Request(path=path, params=p, verb="post").perform()
        )

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
        return Email.new_from_request(
            request.Request(path=path, params={}, verb="get").perform()
        )
