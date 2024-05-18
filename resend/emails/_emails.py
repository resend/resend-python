from typing import Any, Dict, List, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.emails._attachment import Attachment
from resend.emails._email import Email
from resend.emails._tag import Tag

_SendParamsType = TypedDict(
    "_SendParamsType",
    {
        "from": str,
        "to": Union[str, List[str]],
        "subject": str,
        "bcc": NotRequired[Union[List[str], str]],
        "cc": NotRequired[Union[List[str], str]],
        "reply_to": NotRequired[Union[List[str], str]],
        "html": NotRequired[str],
        "text": NotRequired[str],
        "headers": NotRequired[Dict[str, str]],
        "attachments": NotRequired[List[Attachment]],
        "tags": NotRequired[List[Tag]],
    },
)


class Emails:
    class SendParams(_SendParamsType):
        pass

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
        return Email.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params), verb="post"
            ).perform()
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
