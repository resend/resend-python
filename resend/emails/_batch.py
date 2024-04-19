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
        """
        path = "/emails/batch"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform()
        return [Email.new_from_request(val) for val in resp["data"]]
