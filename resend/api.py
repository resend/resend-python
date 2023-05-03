from warnings import warn
from typing import Dict, List

import resend


class Resend:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Resend API Key is required.")
        resend.api_key = api_key

    def send_email(
        self,
        sender: str,
        to,
        subject: str,
        bcc=None,
        cc=None,
        reply_to=None,
        html: str = None,
        text: str = None,
        attachments: List[Dict] = None,
        tags: List[Dict] = None,
    ):
        warn("[DEPRECATION]: method `send_email` is deprecated. Use resend.Emails.send() instead", DeprecationWarning)
        return resend.Emails.send(
            {
                "from": sender,
                "to": to,
                "subject": subject,
                "bcc": bcc,
                "cc": cc,
                "reply_to": reply_to,
                "html": html,
                "text": text,
                "attachments": attachments,
                "tags": tags,
            }
        )
