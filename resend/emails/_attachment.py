from typing import List, Union

from typing_extensions import NotRequired, TypedDict


class Attachment(TypedDict):
    content: Union[List[int], str]
    """
    Content of an attached file.
    This is a list of integers which is usually translated from a
    "bytes" type, OR a string
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
    content_type: NotRequired[str]
    """
    Content type for the attachment, if not set will be derived from the filename property
    """
