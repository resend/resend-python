from typing_extensions import NotRequired, TypedDict


class ReceivedEmailAttachmentDetails(TypedDict):
    """
    ReceivedEmailAttachmentDetails type that wraps a received email attachment with download details.

    Attributes:
        object (str): The object type.
        id (str): The attachment ID.
        filename (str): The filename of the attachment.
        content_type (str): The content type of the attachment.
        content_disposition (str): The content disposition of the attachment.
        content_id (NotRequired[str]): The content ID for inline attachments.
        download_url (str): The URL to download the attachment.
        expires_at (str): When the download URL expires.
    """

    object: str
    """
    The object type.
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
    download_url: str
    """
    The URL to download the attachment.
    """
    expires_at: str
    """
    When the download URL expires.
    """
