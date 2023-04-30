from typing import Dict, List, Union

import resend


class Resend:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Resend API Key is required.")
        resend.api_key = api_key

    def send_email(
        self,
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
    ):
        print(
            "[DEPRECATION]: method `send_email` is deprecated. Use resend.Emails.send() instead"  # noqa
        )
        return resend.Emails.send(
            sender=sender,
            to=to,
            subject=subject,
            bcc=bcc,
            cc=cc,
            reply_to=reply_to,
            html=html,
            text=text,
            attachments=attachments,
            tags=tags,
        )
