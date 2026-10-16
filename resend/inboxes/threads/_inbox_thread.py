from typing import List, Optional

from typing_extensions import TypedDict

from resend._base_response import BaseResponse
from resend.inboxes._inbox import InboxMessageFolder


class InboxThreadLabel(TypedDict):
    """
    InboxThreadLabel is a label attached to a thread.
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


# Functional syntax required because ``from`` is a reserved keyword.
_InboxThreadFrom = TypedDict(
    "_InboxThreadFrom",
    {
        "from": Optional[str],
    },
)


class InboxThread(_InboxThreadFrom):
    """
    InboxThread is a thread as it appears in the list of an inbox's threads.
    The ``from`` key holds the sender email address, and can include the display name.
    """

    id: str
    """
    The ID of the thread.
    """
    subject: Optional[str]
    """
    The subject of the thread.
    """
    to: List[str]
    """
    The recipients of the most recent email. For a received email, these are
    the addresses it was delivered to, not the full ``To`` header.
    """
    cc: List[str]
    """
    The CC recipients of the most recent email.
    """
    bcc: List[str]
    """
    The BCC recipients of the most recent email. Always empty for a received email.
    """
    labels: List[InboxThreadLabel]
    """
    The labels attached to the thread.
    """
    email_count: int
    """
    The number of emails in the thread.
    """
    has_attachment: bool
    """
    Whether the most recent email in the thread has an attachment.
    """
    has_draft: bool
    """
    Whether the thread has an unsent draft.
    """
    read: bool
    """
    True only when every email in the thread is read.
    """
    received_at: str
    """
    Timestamp when the thread was last active.
    """
    folder: InboxMessageFolder
    """
    The folder the thread is in. Every thread is in exactly one folder.
    """


class InboxThreadSearchResult(InboxThread):
    """
    InboxThreadSearchResult is a thread returned by the search threads endpoint.
    """

    matched_email_id: Optional[str]
    """
    The ID of the email in the thread that matched the search. When ``query``
    has words or phrases, it is the most relevant match. Otherwise, it is the
    newest. It is the same ``id`` that the list thread emails endpoint returns,
    so use it as ``email_id`` with the get, reply and forward endpoints.
    None when the search index returns no matched email for the thread.
    """


class InboxThreadSummary(BaseResponse):
    """
    InboxThreadSummary is the summary of a single thread.
    """

    object: str
    """
    The object type. Always ``inbox_thread``.
    """
    id: str
    """
    The ID of the thread.
    """
    subject: Optional[str]
    """
    The subject of the thread.
    """
    folder: InboxMessageFolder
    """
    The folder the thread is in.
    """
    labels: List[InboxThreadLabel]
    """
    The labels attached to the thread.
    """
    read: bool
    """
    True only when every email in the thread is read.
    """
