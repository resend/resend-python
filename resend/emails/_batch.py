from typing import Any, Dict, List, cast
from typing_extensions import TypedDict

from resend import request

from ._email import Email
from ._emails import Emails


class _BatchEmails(TypedDict):
    data: List[Email]
    """
    A list of email objects
    """

class Batch:

    BatchEmails = _BatchEmails

    @classmethod
    def send(cls, params: List[Emails.SendParams]) -> BatchEmails:
        """
        Trigger up to 100 batch emails at once.
        see more: https://resend.com/docs/api-reference/emails/send-batch-emails

        Args:
            params (List[Emails.SendParams]): The list of emails to send

        Returns:
            BatchEmails: A list of email objects
        """
        path = "/emails/batch"

        return cast(_BatchEmails, request.Request(path=path, params=cast(List[Dict[Any, Any]], params), verb="post").perform())