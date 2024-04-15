from typing import List, cast

from typing_extensions import TypedDict, NotRequired

class Email:
    id: str
    """
    The Email ID.
    """
    to: List[str] | str
    """
    List of email addresses to send the email to.
    """
    sender: str
    """
    The email address of the sender. "from" is a reserved keyword in python.
    So we use "sender" here instead
    """
    created_at: str
    """
    When the email was created.
    """
    subject: str
    """
    The subject of the email.
    """
    html: str
    """
    The HTML content of the email.
    """
    text: str
    """
    The text content of the email.
    """
    bcc: List[str] | str
    """
    Bcc
    """
    cc: List[str] | str
    """
    Cc
    """
    reply_to: List[str] | str
    """
    Reply to
    """
    last_event: str
    """
    The last event of the email.
    """

    def __init__(
            self, id, to, sender, created_at, subject,
            html, text, bcc, cc, reply_to, last_event):
        self.id = id
        self.to = to
        self.sender = sender
        self.created_at = created_at
        self.subject = subject
        self.html = html
        self.text = text
        self.bcc = bcc
        self.cc = cc
        self.reply_to = reply_to
        self.last_event = last_event


    @staticmethod
    def new_from_request(val) -> "Email":
        email = Email(
            id=val["id"] if "id" in val else "",
            to=val["to"] if "to" in val else "",

            # we set sender as the value from "from" here
            # because "from" is a reserved keyword in python
            sender=val["from"] if "from" in val else "",

            created_at=val["created_at"] if "created_at" in val else "",
            subject=val["subject"] if "subject" in val else "",
            html=val["html"] if "html" in val else "",
            text=val["text"] if "text" in val else "",
            bcc=val["bcc"] if "bcc" in val else "",
            cc=val["cc"] if "cc" in val else "",
            reply_to=val["reply_to"] if "reply_to" in val else "",
            last_event=val["last_event"] if "last_event" in val else "",
        )
        return email
