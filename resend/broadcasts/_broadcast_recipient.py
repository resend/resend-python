from typing import List, Union

from typing_extensions import Literal, NotRequired, TypedDict

BroadcastRecipientEventType = Literal[
    "sent",
    "delivered",
    "opened",
    "clicked",
    "bounced",
    "complained",
    "unsubscribed",
    "suppressed",
]

BroadcastRecipientBounceType = Literal["permanent", "transient", "undetermined"]


class BroadcastRecipientClickedLink(TypedDict):
    """
    BroadcastRecipientClickedLink represents a link clicked by a broadcast recipient.

    Attributes:
        url (str): The clicked URL.
        clicks (int): The number of times this recipient clicked this URL.
    """

    url: str
    """
    The clicked URL.
    """
    clicks: int
    """
    The number of times this recipient clicked this URL.
    """


class BroadcastRecipient(TypedDict):
    """
    BroadcastRecipient represents a single recipient in a broadcast recipients list.

    Attributes:
        id (str): Opaque cursor identifying this row, used for pagination.
        contact_id (Union[str, None]): The ID of the contact associated with this recipient, if one exists.
        email (str): The recipient's email address.
        count (NotRequired[int]): The number of times this recipient triggered the event.
            Only present when the requested type is "opened" or "clicked".
        bounce_type (NotRequired[BroadcastRecipientBounceType]): The type of bounce.
            Only present when the requested type is "bounced".
        clicked_links (NotRequired[List[BroadcastRecipientClickedLink]]): The links this recipient clicked.
            Only present when the requested type is "clicked".
    """

    id: str
    """
    Opaque cursor identifying this row, used for pagination.
    """
    contact_id: Union[str, None]
    """
    The ID of the contact associated with this recipient, if one exists.
    """
    email: str
    """
    The recipient's email address.
    """
    count: NotRequired[int]
    """
    The number of times this recipient triggered the event.
    Only present when the requested type is "opened" or "clicked".
    """
    bounce_type: NotRequired[BroadcastRecipientBounceType]
    """
    The type of bounce.
    Only present when the requested type is "bounced".
    """
    clicked_links: NotRequired[List[BroadcastRecipientClickedLink]]
    """
    The links this recipient clicked.
    Only present when the requested type is "clicked".
    """
