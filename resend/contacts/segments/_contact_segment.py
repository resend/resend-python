from typing_extensions import TypedDict


class ContactSegment(TypedDict):
    id: str
    """
    The unique identifier of the segment.
    """
    name: str
    """
    The name of the segment.
    """
    created_at: str
    """
    The date and time the segment was created.
    """
