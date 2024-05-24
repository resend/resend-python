from typing import Any, Dict, List, Union

from typing_extensions import TypedDict

# Uses functional typed dict syntax here in order to support "from" reserved keyword
FromParam = TypedDict(
    "FromParam",
    {
        "from": str,
    },
)


class EmailDefault(TypedDict):
    id: str
    """
    The Email ID.
    """
    to: Union[List[str], str]
    """
    List of email addresses to send the email to.
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

class Email(FromParam, EmailDefault):
    pass
