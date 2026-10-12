from typing import List, Optional

from typing_extensions import Literal, TypedDict

from resend._base_response import BaseResponse

InboxDraftType = Literal["standalone", "reply"]
"""
``reply`` when the draft replies to an email in an existing thread.
``standalone`` when the draft starts a new thread.
"""


class InboxDraft(BaseResponse):
    """
    InboxDraft is an unsent or sent draft of an inbox.
    """

    object: str
    """
    The object type. Always ``inbox_draft``.
    """
    id: str
    """
    The ID of the draft.
    """
    type: InboxDraftType
    """
    ``reply`` when the draft replies to an email in an existing thread.
    ``standalone`` when the draft starts a new thread.
    """
    to: Optional[List[str]]
    """
    The recipients. None or empty when no recipients are set.
    """
    cc: List[str]
    """
    The CC recipients.
    """
    bcc: List[str]
    """
    The BCC recipients.
    """
    subject: Optional[str]
    """
    The subject.
    """
    html: Optional[str]
    """
    The HTML body.
    """
    text: Optional[str]
    """
    The plain text body.
    """
    thread_id: Optional[str]
    """
    The Thread ID when the draft is a reply. None otherwise.
    """
    reply_to_email_id: Optional[str]
    """
    The Email ID the draft replies to. None otherwise.
    """
    email_id: Optional[str]
    """
    The ID of the outbound email queued when the draft was sent.
    None until the draft is sent.
    """
    created_at: str
    """
    Timestamp when the draft was created.
    """
    updated_at: str
    """
    Timestamp when the draft was last saved.
    """


class InboxDraftListItem(TypedDict):
    """
    InboxDraftListItem is a draft as it appears in the list of drafts.
    """

    id: str
    """
    The ID of the draft.
    """
    type: InboxDraftType
    """
    ``reply`` when the draft replies to an email in an existing thread.
    ``standalone`` when the draft starts a new thread.
    """
    to: Optional[List[str]]
    """
    The recipients. None or empty when no recipients are set.
    """
    cc: List[str]
    """
    The CC recipients.
    """
    bcc: List[str]
    """
    The BCC recipients.
    """
    subject: Optional[str]
    """
    The subject.
    """
    snippet: Optional[str]
    """
    A short preview of the body.
    """
    thread_id: Optional[str]
    """
    The Thread ID when the draft is a reply. None otherwise.
    """
    reply_to_email_id: Optional[str]
    """
    The Email ID the draft replies to. None otherwise.
    """
    updated_at: str
    """
    Timestamp when the draft was last saved.
    """
