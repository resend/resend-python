from typing import List, Union

from typing_extensions import TypedDict

# Uses functional typed dict syntax here in order to support "from" reserved keyword
_FromParam = TypedDict(
    "_FromParam",
    {
        "from": str,
    },
)


class _EmailDefaultAttrs(_FromParam):
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


class Email(_EmailDefaultAttrs):
    """
    Email type that wraps the email object

    Attributes:
        id (str): The Email ID.
        from (str): The email address the email was sent from.
        to (Union[List[str], str]): List of email addresses to send the email to.
        created_at (str): When the email was created.
        subject (str): The subject of the email.
        html (str): The HTML content of the email.
        text (str): The text content of the email.
        bcc (Union[List[str], str]): Bcc
        cc (Union[List[str], str]): Cc
        reply_to (Union[List[str], str]): Reply to
        last_event (str): The last event of the email.
    """
