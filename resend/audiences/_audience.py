from typing_extensions import TypedDict


class Audience(TypedDict):
    id: str
    """
    The unique identifier of the audience.
    """
    name: str
    """
    The name of the audience.
    """
    created_at: str
    """
    The date and time the audience was created.
    """
