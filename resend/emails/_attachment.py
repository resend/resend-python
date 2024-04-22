from typing import List

from typing_extensions import NotRequired, TypedDict


class Attachment(TypedDict):
    content: List[int]
    """
    Content of an attached file.
    This is a list of integers which is usually translated from a
    "bytes" type.
    Ie: list(open("file.pdf", "rb").read())
    """
    filename: str
    """
    Name of attached file.
    """
    path: NotRequired[str]
    """
    Path where the attachment file is hosted
    """
