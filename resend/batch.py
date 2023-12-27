from typing import Dict, List

from resend import request


class Batch:
    """(Beta) Batch Email sending API Wrapper"""

    @classmethod
    # https://resend.com/docs/api-reference/emails/send-batch-emails
    def send(
        cls,
        params: List[Dict],
    ) -> List[Dict]:
        path = "/emails/batch"
        return request.Request(path=path, params=params, verb="post").perform()
