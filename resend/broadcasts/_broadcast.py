from typing import List, Union

from typing_extensions import TypedDict

# Uses functional typed dict syntax here in order to support "from" reserved keyword
_FromParam = TypedDict(
    "_FromParam",
    {
        "from": str,
    },
)


class Broadcast(_FromParam):
    object: str
    """
    The object type, which is always "broadcast".
    """
    id: str
    """
    The unique identifier of the broadcast.
    """
    segment_id: Union[str, None]
    """
    The unique identifier of the segment.
    """
    audience_id: Union[str, None]
    """
    The unique identifier of the audience.

    .. deprecated::
        Use segment_id instead.
    """
    name: str
    """
    The name of the broadcast.
    """
    subject: str
    """
    The subject of the broadcast.
    """
    reply_to: Union[List[str], str]
    """
    The reply-to email address.
    """
    preview_text: str
    """
    The preview text of the broadcast.
    """
    status: str
    """
    The status of the broadcast.
    """
    created_at: str
    """
    The date and time the broadcast was created.
    """
    scheduled_at: str
    """
    The date and time the broadcast is scheduled to be sent.
    """
    sent_at: str
    """
    The date and time the broadcast was sent.
    """
    html: Union[str, None]
    """
    The HTML content of the broadcast.
    """
    text: Union[str, None]
    """
    The plain text content of the broadcast.
    """
