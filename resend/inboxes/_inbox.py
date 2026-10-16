from typing import Optional

from typing_extensions import Literal, TypedDict

from resend._base_response import BaseResponse

InboxMessageFolder = Literal["inbox", "archive", "spam", "sent", "trash"]
"""
A folder of an inbox. Every thread is in exactly one folder. ``inbox`` holds
threads with at least one received email. ``archive`` and ``spam`` hold threads
moved there. ``trash`` holds threads scheduled for deletion in 30 days. ``sent``
holds threads whose emails are all outbound, and is assigned automatically.
"""

MoveThreadFolder = Literal["inbox", "archive", "spam", "trash"]
"""
A folder a thread can be moved to. ``sent`` is assigned automatically and
cannot be set.
"""


class Inbox(BaseResponse):
    """
    Inbox is the full inbox object, as returned when you retrieve an inbox.
    """

    object: str
    """
    The object type. Always ``inbox``.
    """
    id: str
    """
    The ID of the inbox.
    """
    name: str
    """
    Internal name for the inbox. Recipients do not see it.
    Falls back to the inbox email address.
    """
    email_address: str
    """
    The address of the inbox.
    """
    domain_id: str
    """
    The ID of the domain that owns the address.
    """
    receiving_address: Optional[str]
    """
    The address to forward mail to when forwarding is enabled. None otherwise.
    """
    from_name: Optional[str]
    """
    The name recipients see when mail is sent from this inbox. None when not set.
    """
    unread: int
    """
    The number of unread threads in the Inbox folder.
    """
    drafts: int
    """
    The number of unsent drafts.
    """
    last_received: Optional[str]
    """
    ISO 8601 timestamp of the newest received email in the Inbox folder.
    None when the folder has no received email.
    """
    created_at: str
    """
    ISO 8601 timestamp when the inbox was created.
    """
    updated_at: str
    """
    ISO 8601 timestamp when the inbox was last updated.
    """


class InboxListItem(TypedDict):
    """
    InboxListItem is an inbox as it appears in the list of inboxes.
    It carries fewer fields than a single inbox.
    """

    id: str
    """
    The ID of the inbox.
    """
    name: Optional[str]
    """
    Internal name for the inbox. Recipients do not see it.
    """
    email_address: str
    """
    The address of the inbox.
    """
    from_name: Optional[str]
    """
    The name recipients see when mail is sent from this inbox. None when not set.
    """
    unread: int
    """
    The number of unread threads in the Inbox folder.
    """
    last_received: Optional[str]
    """
    ISO 8601 timestamp of the newest received email in the Inbox folder.
    None when the folder has no received email.
    """
    created_at: str
    """
    ISO 8601 timestamp when the inbox was created.
    """
    updated_at: str
    """
    ISO 8601 timestamp when the inbox was last updated.
    """
