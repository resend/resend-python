from typing import Dict, List, Optional

from typing_extensions import Literal, NotRequired, TypedDict

from resend._base_response import BaseResponse


class EmailAttachment(TypedDict):
    """
    Attachment metadata embedded in a received (inbound) email, as returned by
    ``Emails.Receiving.get`` and ``Emails.Receiving.list``.

    These are raw values from the inbound MIME parts, so ``filename``,
    ``content_id``, and ``content_disposition`` can be null (e.g. S/MIME
    signatures or calendar invites), and ``size`` is null in list responses.

    Attributes:
        id (str): The attachment ID.
        filename (Optional[str]): The filename of the attachment.
        content_type (str): The content type of the attachment.
        content_id (Optional[str]): The content ID for inline attachments.
        content_disposition (Optional[str]): The content disposition of the attachment.
        size (Optional[int]): The size of the attachment in bytes.
    """

    id: str
    """
    The attachment ID.
    """
    filename: Optional[str]
    """
    The filename of the attachment.
    """
    content_type: str
    """
    The content type of the attachment.
    """
    content_id: Optional[str]
    """
    The content ID for inline attachments.
    """
    content_disposition: Optional[str]
    """
    The content disposition of the attachment.
    """
    size: Optional[int]
    """
    The size of the attachment in bytes.
    """


class AttachmentWithSignedUrl(TypedDict):
    """
    Attachment returned by the signed-URL endpoints that list or retrieve
    attachments (for both sent and received emails).

    Attributes:
        id (str): The attachment ID.
        filename (NotRequired[str]): The filename of the attachment.
        content_type (str): The content type of the attachment.
        content_id (NotRequired[str]): The content ID for inline attachments.
        content_disposition (Literal["inline", "attachment"]): The content disposition of the attachment.
        size (int): The size of the attachment in bytes.
        download_url (str): The URL to download the attachment.
        expires_at (str): When the download URL expires.
    """

    id: str
    """
    The attachment ID.
    """
    filename: NotRequired[str]
    """
    The filename of the attachment.
    """
    content_type: str
    """
    The content type of the attachment.
    """
    content_id: NotRequired[str]
    """
    The content ID for inline attachments.
    """
    content_disposition: Literal["inline", "attachment"]
    """
    The content disposition of the attachment.
    """
    size: int
    """
    The size of the attachment in bytes.
    """
    download_url: str
    """
    The URL to download the attachment.
    """
    expires_at: str
    """
    When the download URL expires.
    """


class EmailAttachmentDetails(AttachmentWithSignedUrl):
    """
    A single attachment retrieved from a dedicated attachment endpoint. Same as
    ``AttachmentWithSignedUrl`` with an added ``object`` field.

    Attributes:
        object (str): The object type.
        id (str): The attachment ID.
        filename (NotRequired[str]): The filename of the attachment.
        content_type (str): The content type of the attachment.
        content_id (NotRequired[str]): The content ID for inline attachments.
        content_disposition (Literal["inline", "attachment"]): The content disposition of the attachment.
        size (int): The size of the attachment in bytes.
        download_url (str): The URL to download the attachment.
        expires_at (str): When the download URL expires.
    """

    object: str
    """
    The object type.
    """


# Uses functional typed dict syntax here in order to support "from" reserved keyword
_ReceivedEmailFromParam = TypedDict(
    "_ReceivedEmailFromParam",
    {
        "from": str,
    },
)


# For list responses (omits html, text, headers, object from full email)
_ListReceivedEmailFromParam = TypedDict(
    "_ListReceivedEmailFromParam",
    {
        "from": str,
    },
)


class _ReceivedEmailDefaultAttrs(_ReceivedEmailFromParam, BaseResponse):
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
    message_id: str
    """
    The message ID of the email.
    """
    headers: NotRequired[Dict[str, str]]
    """
    Email headers.
    """
    attachments: List[EmailAttachment]
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
        message_id (str): The message ID of the email.
        headers (NotRequired[Dict[str, str]]): Email headers.
        attachments (List[EmailAttachment]): List of attachments.
    """


class _ListReceivedEmailDefaultAttrs(_ListReceivedEmailFromParam):
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
    message_id: str
    """
    The message ID of the email.
    """
    attachments: List[EmailAttachment]
    """
    List of attachments.
    """


class ListReceivedEmail(_ListReceivedEmailDefaultAttrs):
    """
    ListReceivedEmail type for received email items in list responses.
    Omits html, text, headers, and object fields from the full email.

    Attributes:
        id (str): The received email ID.
        to (List[str]): List of recipient email addresses.
        from (str): The sender email address.
        created_at (str): When the email was received.
        subject (str): The subject of the email.
        bcc (Optional[List[str]]): Bcc recipients.
        cc (Optional[List[str]]): Cc recipients.
        reply_to (Optional[List[str]]): Reply-to addresses.
        message_id (str): The message ID of the email.
        attachments (List[EmailAttachment]): List of attachments.
    """
