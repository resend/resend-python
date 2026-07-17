from typing import Dict, List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

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
    first_name: NotRequired[str]
    """
    The contact's first name.
    """
    last_name: NotRequired[str]
    """
    The contact's last name.
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
    DomainCreatedEvent,
    DomainUpdatedEvent,
    DomainDeletedEvent,
]
"""
Union of all Resend webhook event payload shapes returned by ``Webhooks.verify``.
"""
