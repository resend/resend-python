from typing import Dict, List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

from resend.inboxes._inbox import Inbox, MoveThreadFolder
from resend.inboxes.drafts._inbox_draft import InboxDraftAttachment
from resend.inboxes.threads._inbox_thread import (InboxThreadLabel,
                                                  InboxThreadSummary)
from resend.suppressions._suppression import SuppressionListItem

# Functional syntax required because ``from`` is a reserved keyword.
_FromField = TypedDict(
    "_FromField",
    {
        "from": str,
    },
)


class EmailBounce(TypedDict):
    """
    Bounce details included on ``email.bounced`` webhook events.

    Field names match the API payload (camelCase).
    """

    diagnosticCode: NotRequired[str]  # noqa: N815
    """
    Diagnostic code returned by the receiving server, when available.
    """
    message: str
    """
    Detailed bounce message from the receiving server.
    """
    subType: str  # noqa: N815
    """
    Bounce sub-type (e.g. ``Suppressed``, ``MessageRejected``).
    """
    type: str
    """
    Bounce type (e.g. ``Permanent``, ``Temporary``).
    """


class EmailClick(TypedDict):
    """
    Click tracking details included on ``email.clicked`` webhook events.

    Field names match the API payload (camelCase).
    """

    ipAddress: str  # noqa: N815
    """
    IP address of the user who clicked the link.
    """
    link: str
    """
    The URL that was clicked.
    """
    timestamp: str
    """
    ISO 8601 timestamp when the click occurred.
    """
    userAgent: str  # noqa: N815
    """
    User agent string of the browser that clicked the link.
    """


class EmailFailed(TypedDict):
    """
    Failure details included on ``email.failed`` webhook events.
    """

    reason: str
    """
    Reason for the email failure (e.g. ``reached_daily_quota``).
    """


class EmailSuppressed(TypedDict):
    """
    Suppression details included on ``email.suppressed`` webhook events.
    """

    message: str
    """
    Suppression message.
    """
    type: str
    """
    Suppression type.
    """


class ReceivedEmailAttachment(TypedDict):
    """
    Attachment metadata included on ``email.received`` webhook events.
    """

    id: str
    """
    The attachment ID.
    """
    filename: Optional[str]
    """
    The filename of the attachment.
    """
    content_type: str
    """
    The content type of the attachment.
    """
    content_disposition: Optional[str]
    """
    The content disposition of the attachment.
    """
    content_id: Optional[str]
    """
    The content ID for inline attachments.
    """


class BaseEmailEventData(_FromField):
    """
    Shared ``data`` fields for outbound email webhook events.

    See: https://resend.com/docs/webhooks/emails/sent
    """

    created_at: str
    """
    ISO 8601 timestamp when the email was created.
    """
    email_id: str
    """
    Unique identifier for the specific email.
    """
    message_id: str
    """
    RFC Message-ID header value for the email.
    """
    to: List[str]
    """
    Array of impacted recipient email addresses.
    """
    subject: str
    """
    Email subject line.
    """
    broadcast_id: NotRequired[str]
    """
    Unique identifier for the broadcast campaign (if applicable).
    """
    template_id: NotRequired[str]
    """
    Unique identifier for the template used (if applicable).
    """
    tags: NotRequired[Dict[str, str]]
    """
    Tag key-value pairs associated with the email.
    """


class EmailBouncedEventData(BaseEmailEventData):
    """
    ``data`` payload for ``email.bounced`` events.
    """

    bounce: EmailBounce
    """
    Bounce details from the receiving server.
    """


class EmailClickedEventData(BaseEmailEventData):
    """
    ``data`` payload for ``email.clicked`` events.
    """

    click: EmailClick
    """
    Click tracking details.
    """


class EmailFailedEventData(BaseEmailEventData):
    """
    ``data`` payload for ``email.failed`` events.
    """

    failed: EmailFailed
    """
    Failure details.
    """


class EmailSuppressedEventData(BaseEmailEventData):
    """
    ``data`` payload for ``email.suppressed`` events.
    """

    suppressed: EmailSuppressed
    """
    Suppression details.
    """


class ReceivedEmailEventData(_FromField):
    """
    ``data`` payload for ``email.received`` events.

    See: https://resend.com/docs/webhooks/emails/received
    """

    email_id: str
    """
    Unique identifier for the specific email.
    """
    created_at: str
    """
    ISO 8601 timestamp when the email was created.
    """
    to: List[str]
    """
    Array of recipient email addresses.
    """
    bcc: List[str]
    """
    BCC recipient email addresses.
    """
    cc: List[str]
    """
    CC recipient email addresses.
    """
    received_for: List[str]
    """
    Recipient addresses the email was forwarded for.
    """
    message_id: str
    """
    RFC Message-ID header value for the email.
    """
    subject: str
    """
    Email subject line.
    """
    attachments: List[ReceivedEmailAttachment]
    """
    Attachment metadata (bodies are fetched separately).
    """


class ContactEventData(TypedDict):
    """
    ``data`` payload for contact webhook events.
    """

    id: str
    """
    The contact ID.
    """
    audience_id: str
    """
    The audience ID.
    """
    segment_ids: List[str]
    """
    Segment IDs associated with the contact.
    """
    created_at: str
    """
    When the contact was created.
    """
    updated_at: str
    """
    When the contact was last updated.
    """
    email: str
    """
    The contact email address.
    """
    unsubscribed: bool
    """
    Whether the contact is unsubscribed.
    """
    first_name: NotRequired[Optional[str]]
    """
    The contact's first name. None when the contact has no first name.
    """
    last_name: NotRequired[Optional[str]]
    """
    The contact's last name. None when the contact has no last name.
    """


class ContactTopicSubscription(TypedDict):
    """
    Topic entry on ``contact.topics.updated`` events.
    """

    id: str
    """
    The topic ID.
    """
    subscription: Literal["opt_in", "opt_out"]
    """
    The contact's new subscription to the topic.
    """


class ContactTopicsEventData(TypedDict):
    """
    ``data`` payload for ``contact.topics.updated`` events.
    """

    email: str
    """
    The contact email address.
    """
    topics: List[ContactTopicSubscription]
    """
    The topics changed in this update, each with its new subscription.
    """


class DomainRecord(TypedDict):
    """
    DNS record included on domain webhook events.
    """

    record: str
    """
    The record purpose (e.g. ``SPF``, ``DKIM``).
    """
    name: str
    """
    The DNS record name.
    """
    type: str
    """
    The DNS record type.
    """
    ttl: str
    """
    The DNS record TTL.
    """
    status: str
    """
    The DNS record status.
    """
    value: str
    """
    The DNS record value.
    """
    priority: NotRequired[int]
    """
    Optional MX priority.
    """


class DomainEventData(TypedDict):
    """
    ``data`` payload for domain webhook events.
    """

    id: str
    """
    The domain ID.
    """
    name: str
    """
    The domain name.
    """
    status: str
    """
    The domain status.
    """
    created_at: str
    """
    When the domain was created.
    """
    region: str
    """
    The domain region.
    """
    records: List[DomainRecord]
    """
    DNS records associated with the domain.
    """


class SuppressionEventData(SuppressionListItem):
    """
    ``data`` payload for suppression webhook events.

    Same shape as ``SuppressionListItem``: ``id``, ``email``, ``origin``,
    ``source_id``, ``created_at``.
    """


class TopicEventData(TypedDict):
    """
    ``data`` payload for topic webhook events.
    """

    id: str
    """
    The topic ID.
    """
    name: str
    """
    The topic name.
    """
    description: Optional[str]
    """
    The topic description. None when the topic has no description.
    """
    default_subscription: Literal["opt_in", "opt_out"]
    """
    The default subscription preference for new contacts.
    """
    deleted: bool
    """
    Whether the topic is deleted. True on ``topic.deleted`` events.
    """
    created_at: str
    """
    When the topic was created.
    """
    updated_at: str
    """
    When the topic was last updated.
    """


InboxEventSource = Literal["api", "dashboard", "agent", "system"]
"""
What made the change on an inbox webhook event.
"""


class InboxEventEmailAttachment(TypedDict):
    """
    An attachment on an email in an inbox webhook event.
    """

    id: str
    """
    The ID of the attachment.
    """
    filename: Optional[str]
    """
    The filename of the attachment.
    """
    size: Optional[int]
    """
    The size of the attachment in bytes.
    """


class InboxEventEmail(_FromField):
    """
    The email carried by an inbox webhook event. It has no ``html`` or ``text``.
    The ``from`` key holds the sender, as an address or as ``Name <address>``.
    """

    id: str
    """
    The ID of the email.
    """
    direction: Literal["inbound", "outbound"]
    """
    Whether the email was received by the inbox or sent from it.
    """
    to: List[str]
    """
    The recipients of the email.
    """
    cc: List[str]
    """
    The CC recipients of the email.
    """
    bcc: List[str]
    """
    The BCC recipients of the email.
    """
    reply_to: List[str]
    """
    The Reply-To addresses.
    """
    subject: Optional[str]
    """
    The subject of the email.
    """
    message_id: Optional[str]
    """
    The Message-ID header of the email.
    """
    attachments: List[InboxEventEmailAttachment]
    """
    The attachments on the email.
    """
    read: bool
    """
    Whether the email has been read.
    """
    received_at: str
    """
    Timestamp when the email arrived or was sent.
    """


class InboxEventDraft(TypedDict):
    """
    The draft carried by an inbox webhook event. It has no ``html`` or ``text``.
    """

    object: str
    """
    The object type. Always ``inbox_draft``.
    """
    id: str
    """
    The ID of the draft.
    """
    type: Literal["standalone", "reply"]
    """
    ``standalone`` for a new conversation, or ``reply``.
    """
    to: Optional[List[str]]
    """
    The recipients.
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
    thread_id: Optional[str]
    """
    The ID of the thread when this draft is a reply. None otherwise.
    """
    reply_to_email_id: Optional[str]
    """
    The ID of the email this draft replies to. None otherwise.
    """
    email_id: Optional[str]
    """
    The ID of the queued outbound email after send. None until then.
    """
    created_at: str
    """
    Timestamp when the draft was created.
    """
    updated_at: str
    """
    Timestamp when the draft was last saved.
    """
    attachments: List[InboxDraftAttachment]
    """
    The files stored on the draft.
    """


class InboxEventData(TypedDict):
    """
    ``data`` payload for ``inbox.created`` and ``inbox.updated`` events.
    """

    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    inbox: NotRequired[Inbox]
    """
    The inbox as it is when the webhook is sent. Absent when the inbox no longer exists.
    """


class InboxDeletedEventData(TypedDict):
    """
    ``data`` payload for ``inbox.deleted`` events.
    """

    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """


class InboxThreadEmailEventData(TypedDict):
    """
    ``data`` payload for ``inbox.thread.created``, ``inbox.email.received`` and
    ``inbox.email.sent`` events.
    """

    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    thread_id: str
    """
    The ID of the thread.
    """
    email_id: str
    """
    The ID of the email.
    """
    thread: NotRequired[InboxThreadSummary]
    """
    The thread as it is when the webhook is sent. Absent when the thread no longer exists.
    """
    email: NotRequired[InboxEventEmail]
    """
    The email as it is when the webhook is sent, without ``html`` or ``text``.
    Fetch the body with ``Inboxes.Threads.Emails.get``. Absent when the email no
    longer exists.
    """


# Functional syntax required because ``from`` is a reserved keyword.
_InboxThreadFolderMove = TypedDict(
    "_InboxThreadFolderMove",
    {
        "from": MoveThreadFolder,
        "to": MoveThreadFolder,
    },
)


class InboxThreadFolderUpdatedEventData(_InboxThreadFolderMove):
    """
    ``data`` payload for ``inbox.thread.folder.updated`` events. The ``from`` key
    holds the folder the thread was in, and ``to`` the folder it moved to.
    """

    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    thread_id: str
    """
    The ID of the thread.
    """
    thread: NotRequired[InboxThreadSummary]
    """
    The thread as it is when the webhook is sent. Absent when the thread no longer exists.
    """


class InboxThreadAssignedEventData(TypedDict):
    """
    ``data`` payload for ``inbox.thread.assigned`` events.
    """

    assignee_email: Optional[str]
    """
    The email of the member the thread is now assigned to.
    """
    assigned_by_email: Optional[str]
    """
    The email of the member who made the assignment. None when no member made it.
    """
    previous_assignee_email: Optional[str]
    """
    The email of the member the thread was assigned to before. None when it was unassigned.
    """
    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    thread_id: str
    """
    The ID of the thread.
    """
    thread: NotRequired[InboxThreadSummary]
    """
    The thread as it is when the webhook is sent. Absent when the thread no longer exists.
    """


class InboxThreadUnassignedEventData(TypedDict):
    """
    ``data`` payload for ``inbox.thread.unassigned`` events.
    """

    previous_assignee_email: Optional[str]
    """
    The email of the member the thread was assigned to.
    """
    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    thread_id: str
    """
    The ID of the thread.
    """
    thread: NotRequired[InboxThreadSummary]
    """
    The thread as it is when the webhook is sent. Absent when the thread no longer exists.
    """


class InboxThreadLabelsUpdatedEventData(TypedDict):
    """
    ``data`` payload for ``inbox.thread.labels.updated`` events.
    One event carries one label, in either ``added`` or ``removed``.
    """

    added: List[InboxThreadLabel]
    """
    The labels applied to the thread.
    """
    removed: List[InboxThreadLabel]
    """
    The labels removed from the thread.
    """
    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    thread_id: str
    """
    The ID of the thread.
    """
    thread: NotRequired[InboxThreadSummary]
    """
    The thread as it is when the webhook is sent. Absent when the thread no longer exists.
    """


class InboxDraftEventData(TypedDict):
    """
    ``data`` payload for ``inbox.draft.created``, ``inbox.draft.updated`` and
    ``inbox.draft.deleted`` events.
    """

    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    thread_id: NotRequired[str]
    """
    The ID of the thread. Only on reply drafts.
    """
    draft_id: str
    """
    The ID of the draft.
    """
    thread: NotRequired[InboxThreadSummary]
    """
    The thread as it is when the webhook is sent. Absent when the thread no
    longer exists. Only on reply drafts.
    """
    draft: NotRequired[InboxEventDraft]
    """
    The draft as it is when the webhook is sent, without ``html`` or ``text``.
    Fetch the body with ``Inboxes.Drafts.get``. Absent when the draft no longer exists.
    """


class InboxDraftSentEventData(TypedDict):
    """
    ``data`` payload for ``inbox.draft.sent`` events.
    """

    source: InboxEventSource
    """
    What made the change.
    """
    inbox_id: str
    """
    The ID of the inbox.
    """
    thread_id: str
    """
    The ID of the thread.
    """
    email_id: str
    """
    The ID of the email.
    """
    draft_id: str
    """
    The ID of the draft.
    """
    thread: NotRequired[InboxThreadSummary]
    """
    The thread as it is when the webhook is sent. Absent when the thread no longer exists.
    """
    email: NotRequired[InboxEventEmail]
    """
    The email as it is when the webhook is sent, without ``html`` or ``text``.
    Fetch the body with ``Inboxes.Threads.Emails.get``. Only when the email is
    already on the thread when the webhook is sent.
    """
    draft: NotRequired[InboxEventDraft]
    """
    The draft as it is when the webhook is sent, without ``html`` or ``text``.
    Fetch the body with ``Inboxes.Drafts.get``. Absent when the draft no longer exists.
    """


class EmailSentEvent(TypedDict):
    """Webhook payload for ``email.sent``."""

    type: Literal["email.sent"]
    created_at: str
    data: BaseEmailEventData


class EmailScheduledEvent(TypedDict):
    """Webhook payload for ``email.scheduled``."""

    type: Literal["email.scheduled"]
    created_at: str
    data: BaseEmailEventData


class EmailDeliveredEvent(TypedDict):
    """Webhook payload for ``email.delivered``."""

    type: Literal["email.delivered"]
    created_at: str
    data: BaseEmailEventData


class EmailDeliveryDelayedEvent(TypedDict):
    """Webhook payload for ``email.delivery_delayed``."""

    type: Literal["email.delivery_delayed"]
    created_at: str
    data: BaseEmailEventData


class EmailComplainedEvent(TypedDict):
    """Webhook payload for ``email.complained``."""

    type: Literal["email.complained"]
    created_at: str
    data: BaseEmailEventData


class EmailBouncedEvent(TypedDict):
    """Webhook payload for ``email.bounced``."""

    type: Literal["email.bounced"]
    created_at: str
    data: EmailBouncedEventData


class EmailOpenedEvent(TypedDict):
    """Webhook payload for ``email.opened``."""

    type: Literal["email.opened"]
    created_at: str
    data: BaseEmailEventData


class EmailClickedEvent(TypedDict):
    """Webhook payload for ``email.clicked``."""

    type: Literal["email.clicked"]
    created_at: str
    data: EmailClickedEventData


class EmailReceivedEvent(TypedDict):
    """Webhook payload for ``email.received``."""

    type: Literal["email.received"]
    created_at: str
    data: ReceivedEmailEventData


class EmailFailedEvent(TypedDict):
    """Webhook payload for ``email.failed``."""

    type: Literal["email.failed"]
    created_at: str
    data: EmailFailedEventData


class EmailSuppressedEvent(TypedDict):
    """Webhook payload for ``email.suppressed``."""

    type: Literal["email.suppressed"]
    created_at: str
    data: EmailSuppressedEventData


class ContactCreatedEvent(TypedDict):
    """Webhook payload for ``contact.created``."""

    type: Literal["contact.created"]
    created_at: str
    data: ContactEventData


class ContactUpdatedEvent(TypedDict):
    """Webhook payload for ``contact.updated``."""

    type: Literal["contact.updated"]
    created_at: str
    data: ContactEventData


class ContactDeletedEvent(TypedDict):
    """Webhook payload for ``contact.deleted``."""

    type: Literal["contact.deleted"]
    created_at: str
    data: ContactEventData


class ContactTopicsUpdatedEvent(TypedDict):
    """Webhook payload for ``contact.topics.updated``."""

    type: Literal["contact.topics.updated"]
    created_at: str
    data: ContactTopicsEventData


class DomainCreatedEvent(TypedDict):
    """Webhook payload for ``domain.created``."""

    type: Literal["domain.created"]
    created_at: str
    data: DomainEventData


class DomainUpdatedEvent(TypedDict):
    """Webhook payload for ``domain.updated``."""

    type: Literal["domain.updated"]
    created_at: str
    data: DomainEventData


class DomainDeletedEvent(TypedDict):
    """Webhook payload for ``domain.deleted``."""

    type: Literal["domain.deleted"]
    created_at: str
    data: DomainEventData


class SuppressionAddedEvent(TypedDict):
    """Webhook payload for ``suppression.added``."""

    type: Literal["suppression.added"]
    created_at: str
    data: SuppressionEventData


class SuppressionRemovedEvent(TypedDict):
    """Webhook payload for ``suppression.removed``."""

    type: Literal["suppression.removed"]
    created_at: str
    data: SuppressionEventData


class TopicCreatedEvent(TypedDict):
    """Webhook payload for ``topic.created``."""

    type: Literal["topic.created"]
    created_at: str
    data: TopicEventData


class TopicUpdatedEvent(TypedDict):
    """Webhook payload for ``topic.updated``."""

    type: Literal["topic.updated"]
    created_at: str
    data: TopicEventData


class TopicDeletedEvent(TypedDict):
    """Webhook payload for ``topic.deleted``."""

    type: Literal["topic.deleted"]
    created_at: str
    data: TopicEventData


class InboxCreatedEvent(TypedDict):
    """Webhook payload for ``inbox.created``."""

    type: Literal["inbox.created"]
    created_at: str
    data: InboxEventData


class InboxUpdatedEvent(TypedDict):
    """Webhook payload for ``inbox.updated``."""

    type: Literal["inbox.updated"]
    created_at: str
    data: InboxEventData


class InboxDeletedEvent(TypedDict):
    """Webhook payload for ``inbox.deleted``."""

    type: Literal["inbox.deleted"]
    created_at: str
    data: InboxDeletedEventData


class InboxThreadCreatedEvent(TypedDict):
    """Webhook payload for ``inbox.thread.created``."""

    type: Literal["inbox.thread.created"]
    created_at: str
    data: InboxThreadEmailEventData


class InboxEmailReceivedEvent(TypedDict):
    """Webhook payload for ``inbox.email.received``."""

    type: Literal["inbox.email.received"]
    created_at: str
    data: InboxThreadEmailEventData


class InboxEmailSentEvent(TypedDict):
    """Webhook payload for ``inbox.email.sent``."""

    type: Literal["inbox.email.sent"]
    created_at: str
    data: InboxThreadEmailEventData


class InboxThreadFolderUpdatedEvent(TypedDict):
    """Webhook payload for ``inbox.thread.folder.updated``."""

    type: Literal["inbox.thread.folder.updated"]
    created_at: str
    data: InboxThreadFolderUpdatedEventData


class InboxThreadAssignedEvent(TypedDict):
    """Webhook payload for ``inbox.thread.assigned``."""

    type: Literal["inbox.thread.assigned"]
    created_at: str
    data: InboxThreadAssignedEventData


class InboxThreadUnassignedEvent(TypedDict):
    """Webhook payload for ``inbox.thread.unassigned``."""

    type: Literal["inbox.thread.unassigned"]
    created_at: str
    data: InboxThreadUnassignedEventData


class InboxThreadLabelsUpdatedEvent(TypedDict):
    """Webhook payload for ``inbox.thread.labels.updated``."""

    type: Literal["inbox.thread.labels.updated"]
    created_at: str
    data: InboxThreadLabelsUpdatedEventData


class InboxDraftCreatedEvent(TypedDict):
    """Webhook payload for ``inbox.draft.created``."""

    type: Literal["inbox.draft.created"]
    created_at: str
    data: InboxDraftEventData


class InboxDraftUpdatedEvent(TypedDict):
    """Webhook payload for ``inbox.draft.updated``."""

    type: Literal["inbox.draft.updated"]
    created_at: str
    data: InboxDraftEventData


class InboxDraftSentEvent(TypedDict):
    """Webhook payload for ``inbox.draft.sent``."""

    type: Literal["inbox.draft.sent"]
    created_at: str
    data: InboxDraftSentEventData


class InboxDraftDeletedEvent(TypedDict):
    """Webhook payload for ``inbox.draft.deleted``."""

    type: Literal["inbox.draft.deleted"]
    created_at: str
    data: InboxDraftEventData


WebhookEventPayload = Union[
    EmailSentEvent,
    EmailScheduledEvent,
    EmailDeliveredEvent,
    EmailDeliveryDelayedEvent,
    EmailComplainedEvent,
    EmailBouncedEvent,
    EmailOpenedEvent,
    EmailClickedEvent,
    EmailReceivedEvent,
    EmailFailedEvent,
    EmailSuppressedEvent,
    ContactCreatedEvent,
    ContactUpdatedEvent,
    ContactDeletedEvent,
    ContactTopicsUpdatedEvent,
    DomainCreatedEvent,
    DomainUpdatedEvent,
    DomainDeletedEvent,
    SuppressionAddedEvent,
    SuppressionRemovedEvent,
    TopicCreatedEvent,
    TopicUpdatedEvent,
    TopicDeletedEvent,
    InboxCreatedEvent,
    InboxUpdatedEvent,
    InboxDeletedEvent,
    InboxThreadCreatedEvent,
    InboxEmailReceivedEvent,
    InboxEmailSentEvent,
    InboxThreadFolderUpdatedEvent,
    InboxThreadAssignedEvent,
    InboxThreadUnassignedEvent,
    InboxThreadLabelsUpdatedEvent,
    InboxDraftCreatedEvent,
    InboxDraftUpdatedEvent,
    InboxDraftSentEvent,
    InboxDraftDeletedEvent,
]
"""
Union of all Resend webhook event payload shapes returned by ``Webhooks.verify``.
"""
