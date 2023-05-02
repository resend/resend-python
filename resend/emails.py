from typing import Dict

from resend import request


class Emails:
    """Emails API Wrapper"""

    @classmethod
    # https://resend.com/docs/api-reference/emails/send-email
    def send(
        cls,
        params: Dict,
    ) -> Dict:
        path = "/emails"
        return request.Request(path=path, params=params, verb="post").perform()

    @classmethod
    # https://resend.com/docs/api-reference/emails/retrieve-email
    def get(cls, email_id: str = "") -> Dict:
        path = f"/emails/{email_id}"
        return request.Request(path=path, params={}, verb="get").perform()
