from typing import Any, Dict, List, cast
from typing_extensions import TypedDict

from resend import request

from ._email import Email
from ._emails import Emails

class _SendResponse(TypedDict):
    data: List[Email]
    """
    A list of email objects
    """

class Batch:

    class SendResponse(_SendResponse):
        """
        SendResponse type that wraps a list of email objects

        Attributes:
            data (List[Email]): A list of email objects
        """

    @classmethod
    def send(cls, params: List[Emails.SendParams]) -> SendResponse:
        """
        Trigger up to 100 batch emails at once.
        see more: https://resend.com/docs/api-reference/emails/send-batch-emails

        Args:
            params (List[Emails.SendParams]): The list of emails to send

        Returns:
            SendResponse: A list of email objects
        """
        path = "/emails/batch"

        return cast(_SendResponse, request.Request(path=path, params=cast(List[Dict[Any, Any]], params), verb="post").perform())