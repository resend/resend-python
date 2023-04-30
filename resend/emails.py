from typing import Dict, List, Union

from resend import request


class Emails:
    """Emails API Wrapper"""

    @classmethod
    # https://resend.com/docs/api-reference/emails/send-email
    def send(
        cls,
        sender: str,
        to: Union[str, List[str]],
        subject: str,
        bcc: Union[str, List[str]] = None,
        cc: Union[str, List[str]] = None,
        reply_to: str = None,
        html: str = None,
        text: str = None,
        attachments: List[Dict] = None,
        tags: List[Dict] = None,
    ) -> Dict:
        path = "/emails"

        params: Dict = {"to": to, "from": sender, "subject": subject}
        if text:
            params["text"] = text
        elif html:
            params["html"] = html

        if cc:
            params["cc"] = cc
        if cc:
            params["cc"] = cc
        if bcc:
            params["bcc"] = bcc
        if reply_to:
            params["reply_to"] = reply_to
        if attachments:
            params["attachments"] = attachments
        if tags:
            params["tags"] = tags

        return request.Request(path=path, params=params, verb="post").perform()

    @classmethod
    # https://resend.com/docs/api-reference/emails/retrieve-email
    def get(cls, email_id: str = "") -> Dict:
        path = f"/emails/{email_id}"
        return request.Request(path=path, params={}, verb="get").perform()
