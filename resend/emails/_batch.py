from typing import Any, Dict, List, cast

from resend import request

from ._email import Email
from ._emails import Emails


class Batch:
    @classmethod
    def send(cls, params: List[Emails.SendParams]) -> List[Email]:
        """
        Trigger up to 100 batch emails at once.
        see more: https://resend.com/docs/api-reference/emails/send-batch-emails

        Args:
            params (List[Emails.SendParams]): The list of emails to send

        Returns:
            List[Email]: A list of email objects
        """
        path = "/emails/batch"

        return cast(List[Email], request.Request(path=path, params=cast(List[Dict[Any, Any]], params), verb="post").perform())