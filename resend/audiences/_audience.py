from typing_extensions import Literal, TypedDict

AudienceObject = Literal["audience"]


class ShortAudience(TypedDict):
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


class Audience(ShortAudience):
    object: AudienceObject
    """
    The object type
    """
