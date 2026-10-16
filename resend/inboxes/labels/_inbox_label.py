from typing_extensions import TypedDict


class InboxLabel(TypedDict):
    """
    InboxLabel is a named, colored tag that belongs to one inbox.
    """

    id: str
    """
    The ID of the label.
    """
    name: str
    """
    The name of the label.
    """
    color: str
    """
    The color of the label, as a ``#RRGGBB`` hex color in uppercase.
    """
    created_at: str
    """
    Timestamp when the label was created.
    """
