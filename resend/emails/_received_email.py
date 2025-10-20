from typing import Dict, List, Optional

from typing_extensions import NotRequired, TypedDict


class ReceivedEmailAttachment(TypedDict):
    """
    ReceivedEmailAttachment type that wraps an attachment object from a received email.

    Attributes:
        id (str): The attachment ID.
        filename (str): The filename of the attachment.
        content_type (str): The content type of the attachment.
        content_disposition (str): The content disposition of the attachment.
        content_id (NotRequired[str]): The content ID for inline attachments.
    """

    id: str
    """
    The attachment ID.
    """
    filename: str
    """
    The filename of the attachment.
    """
    content_type: str
    """
    The content type of the attachment.
    """
    content_disposition: str
    """
    The content disposition of the attachment.
    """
    content_id: NotRequired[str]
    """
    The content ID for inline attachments.
    """


# Uses functional typed dict syntax here in order to support "from" reserved keyword
_ReceivedEmailFromParam = TypedDict(
    "_ReceivedEmailFromParam",
    {
        "from": str,
    },
)


class _ReceivedEmailDefaultAttrs(_ReceivedEmailFromParam):
    object: str
    """
    The object type.
    """
    id: str
    """
    The received email ID.
    """
    to: List[str]
    """
    List of recipient email addresses.
    """
    created_at: str
    """
    When the email was received.
    """
    subject: str
    """
    The subject of the email.
    """
    html: Optional[str]
    """
    The HTML content of the email.
    """
    text: Optional[str]
    """
    The text content of the email.
    """
    bcc: Optional[List[str]]
    """
    Bcc recipients.
    """
    cc: Optional[List[str]]
    """
    Cc recipients.
    """
    reply_to: Optional[List[str]]
    """
    Reply-to addresses.
    """
    headers: NotRequired[Dict[str, str]]
    """
    Email headers.
    """
    attachments: List[ReceivedEmailAttachment]
    """
    List of attachments.
    """


class ReceivedEmail(_ReceivedEmailDefaultAttrs):
    """
    ReceivedEmail type that wraps a received (inbound) email object.

    Attributes:
        object (str): The object type.
        id (str): The received email ID.
        to (List[str]): List of recipient email addresses.
        from (str): The sender email address.
        created_at (str): When the email was received.
        subject (str): The subject of the email.
        html (Optional[str]): The HTML content of the email.
        text (Optional[str]): The text content of the email.
        bcc (Optional[List[str]]): Bcc recipients.
        cc (Optional[List[str]]): Cc recipients.
        reply_to (Optional[List[str]]): Reply-to addresses.
        headers (NotRequired[Dict[str, str]]): Email headers.
        attachments (List[ReceivedEmailAttachment]): List of attachments.
    """
