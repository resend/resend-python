from typing_extensions import TypedDict


class Attachment(TypedDict):
    content: str
    """
    Content of an attached file.
    """
    filename: str
    """
    Name of attached file.
    """
    path: str
    """
    Path where the attachment file is hosted
    """
