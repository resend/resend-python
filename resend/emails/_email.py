from typing import Any, Dict, List, Union


class Email:
    id: str
    """
    The Email ID.
    """
    to: Union[List[str], str]
    """
    List of email addresses to send the email to.
    """
    from_: str
    """
    The email address of the sender.
    "from" is a reserved keyword in python.
    So accept either "from_" or "sender"
    """
    sender: str
    """
    The email address of the sender. "from" is a reserved keyword in python.
    So accept either "from_" or "sender"
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
    bcc: Union[List[str], str]
    """
    Bcc
    """
    cc: Union[List[str], str]
    """
    Cc
    """
    reply_to: Union[List[str], str]
    """
    Reply to
    """
    last_event: str
    """
    The last event of the email.
    """

    def __init__(
        self,
        id: str,
        to: Union[List[str], str],
        from_: str,
        sender: str,
        created_at: str,
        subject: str,
        html: str,
        text: str,
        bcc: Union[List[str], str],
        cc: Union[List[str], str],
        reply_to: Union[List[str], str],
        last_event: str,
    ):
        self.id = id
        self.to = to
        self.from_ = from_
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
    def new_from_request(val: Dict[Any, Any]) -> "Email":
        """Creates a new Email object from the
        JSON response from the API.

        Args:
            val (Dict): The JSON response from the API

        Returns:
            Email: The new Email object
        """
        email = Email(
            id=val["id"] if "id" in val else "",
            to=val["to"] if "to" in val else "",
            # from is a reserved keyword in python
            # so we set both from_ and sender here
            from_=val["from"] if "from" in val else "",
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
