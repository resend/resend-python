from typing import Dict, List, cast, Any
from typing_extensions import TypedDict, NotRequired
from resend import request
from resend.emails._email import Email
from resend.emails._tag import Tag
from resend.emails._attachment import Attachment

class Emails:

    class SendParams(TypedDict):
        sender: str
        """
        The email address of the sender.
        "from" is a reserved keyword in python, so we use "sender" here instead
        """
        to: str | List[str]
        """
        List of email addresses to send the email to.
        """
        subject: str
        """
        The subject of the email.
        """
        bcc: NotRequired[List[str] | str]
        """
        Bcc
        """
        cc: NotRequired[List[str] | str]
        """
        Cc
        """
        reply_to: NotRequired[List[str] | str]
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


    @classmethod
    def send(cls, params: SendParams) -> Email:
        """
        Send an email through the Resend Email API.
        see more: https://resend.com/docs/api-reference/emails/send-email
        """
        path = "/emails"

        # we need this workaround here because from is a reserved keyword
        # in python, so we need to use "sender" on the SendParams
        params["from"] = params["sender"] # type: ignore
        return Email.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params),
                verb="post"
            ).perform()
        )

    # @classmethod
    # # https://resend.com/docs/api-reference/emails/retrieve-email
    # def get(cls, email_id: str = "") -> Dict:
    #     path = f"/emails/{email_id}"
    #     return request.Request(path=path, params={}, verb="get").perform()
