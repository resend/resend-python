from typing import List, Optional

from typing_extensions import Literal, TypedDict

from resend._base_response import BaseResponse


class InboxThreadEmailAttachment(TypedDict):
    """
    InboxThreadEmailAttachment is an attachment of a thread email.
    """

    id: str
    """
    The ID of the attachment.
    """
    filename: Optional[str]
    """
    The filename of the attachment.
    """
    size: Optional[int]
    """
    The size of the attachment in bytes.
    """


# Functional syntax required because ``from`` is a reserved keyword.
_InboxThreadEmailFrom = TypedDict(
    "_InboxThreadEmailFrom",
    {
        "from": str,
    },
)


class InboxThreadEmail(_InboxThreadEmailFrom, BaseResponse):
    """
    InboxThreadEmail is a message of an inbox thread.
    The ``from`` key holds the sender email address. It includes the display
    name when the sender has one, in the format "Name <sender@domain.com>".
    """

    id: str
    """
    The ID of the message.
    """
    direction: Literal["inbound", "outbound"]
    """
    Whether the inbox received the message (``inbound``) or sent it (``outbound``).
    A message the inbox sent to itself is ``inbound``, so a reply to it goes to its sender.
    """
    to: List[str]
    """
    The recipients of the message. For a received message, these are the
    addresses it was delivered to, not the full ``To`` header.
    """
    cc: List[str]
    """
    The CC recipients of the message.
    """
    bcc: List[str]
    """
    The BCC recipients of the message. Always empty for a received message.
    """
    reply_to: List[str]
    """
    The Reply-To addresses of the message.
    """
    subject: Optional[str]
    """
    The subject of the message.
    """
    message_id: Optional[str]
    """
    The Message-ID header of the message.
    """
    html: Optional[str]
    """
    The HTML body.
    """
    text: Optional[str]
    """
    The plain-text body.
    """
    attachments: List[InboxThreadEmailAttachment]
    """
    The attachments of the message.
    """
    read: bool
    """
    Whether the message has been read.
    """
    received_at: str
    """
    Timestamp when the inbox received the message, or when the inbox sent it.
    """
