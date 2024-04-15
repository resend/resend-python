from typing_extensions import TypedDict, NotRequired

class Tag(TypedDict):
    name: str
    """
    The name of the email tag.
    It can only contain ASCII letters (a–z, A–Z), numbers (0–9),
    underscores (_), or dashes (-).
    It can contain no more than 256 characters.
    """
    value: NotRequired[str]
    """
    The value of the email tag.
    It can only contain ASCII letters (a–z, A–Z), numbers (0–9),
    underscores (_), or dashes (-).
    It can contain no more than 256 characters.
    """
