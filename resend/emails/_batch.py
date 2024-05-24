from typing import Any, Dict, List, cast

from resend import request

from ._email import Email
from ._emails import Emails


class Batch:
    # @classmethod
    # def send(cls, params: List[Emails.SendParams]) -> List[Email]:
    #     """
    #     Trigger up to 100 batch emails at once.
    #     see more: https://resend.com/docs/api-reference/emails/send-batch-emails

    #     Args:
    #         params (List[Emails.SendParams]): The list of emails to send

    #     Returns:
    #         List[Email]: A list of email objects
    #     """
    #     path = "/emails/batch"

    #     # loop through the list of params and replace "from_" or "sender" with "from"
    #     # if they're present
    #     replaced_params = [
    #         replace_params(cast(Dict[Any, Any], param)) for param in params
    #     ]

    #     resp = request.Request(path=path, params=replaced_params, verb="post").perform()
    #     return [Email.new_from_request(val) for val in resp["data"]]
    pass