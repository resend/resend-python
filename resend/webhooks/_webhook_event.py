from typing import Dict, List, Union

from typing_extensions import Literal, NotRequired, TypedDict


# Uses functional typed dict syntax here in order to support "from" reserved keyword
_BaseEmailEventDataFromParam = TypedDict(
    "_BaseEmailEventDataFromParam",
    {
        "from": str,
    },
)


class BaseEmailEventData(_BaseEmailEventDataFromParam):
    """
    Common fields shared by outbound email webhook event payloads.

    Attributes:
        created_at (str): ISO 8601 timestamp when the email was created.
        email_id (str): Unique identifier for the specific email.
        message_id (str): RFC Message-ID header value for the email.
        from (str): Sender's email address.
        to (List[str]): Array of impacted recipient email addresses.
        subject (str): Email subject line.
        broadcast_id (NotRequired[str]): Unique identifier for the broadcast campaign.
        template_id (NotRequired[str]): Unique identifier for the template used.
        tags (NotRequired[Dict[str, str]]): Tag key-value pairs associated with the email.
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
    Unique identifier for the broadcast campaign.
    """
    template_id: NotRequired[str]
    """
    Unique identifier for the template used.
    """
    tags: NotRequired[Dict[str, str]]
    """
    Tag key-value pairs associated with the email.
    """


class EmailBounce(TypedDict):
    """
    Bounce details from the receiving server.

    Attributes:
        message (str): Detailed bounce message from the receiving server.
        subType (str): Bounce sub-type (e.g., Suppressed, MessageRejected).
        type (str): Bounce type (e.g., Permanent, Temporary).
    """

    message: str
    """
    Detailed bounce message from the receiving server.
    """
    subType: str
    """
    Bounce sub-type (e.g., Suppressed, MessageRejected).
    """
    type: str
    """
    Bounce type (e.g., Permanent, Temporary).
    """


class EmailClick(TypedDict):
    """
    Click tracking details.

    Attributes:
        ipAddress (str): IP address of the user who clicked the link.
        link (str): The URL that was clicked.
        timestamp (str): ISO 8601 timestamp when the click occurred.
        userAgent (str): User agent string of the browser that clicked the link.
    """

    ipAddress: str
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
    userAgent: str
    """
    User agent string of the browser that clicked the link.
    """


class EmailFailed(TypedDict):
    """
    Failure details for an email that failed to send.

    Attributes:
        reason (str): The reason the email failed.
    """

    reason: str
    """
    The reason the email failed.
    """


class EmailSuppressed(TypedDict):
    """
    Suppression details for an email that was not sent.

    Attributes:
        message (str): The suppression message.
        type (str): The suppression type.
    """

    message: str
    """
    The suppression message.
    """
    type: str
    """
    The suppression type.
    """


class ReceivedEmailAttachment(TypedDict):
    """
    Attachment metadata included in email.received webhook payloads.

    Attributes:
        id (str): The attachment ID.
        filename (Union[str, None]): The filename of the attachment.
        content_type (str): The content type of the attachment.
        content_disposition (Union[str, None]): The content disposition of the attachment.
        content_id (Union[str, None]): The content ID for inline attachments.
    """

    id: str
    """
    The attachment ID.
    """
    filename: Union[str, None]
    """
    The filename of the attachment.
    """
    content_type: str
    """
    The content type of the attachment.
    """
    content_disposition: Union[str, None]
    """
    The content disposition of the attachment.
    """
    content_id: Union[str, None]
    """
    The content ID for inline attachments.
    """


_ReceivedEmailEventDataFromParam = TypedDict(
    "_ReceivedEmailEventDataFromParam",
    {
        "from": str,
    },
)


class ReceivedEmailEventData(_ReceivedEmailEventDataFromParam):
    """
    Data payload for email.received webhook events.

    Attributes:
        email_id (str): Unique identifier for the specific email.
        created_at (str): ISO 8601 timestamp when the email was received.
        from (str): Sender's email address.
        to (List[str]): Recipient email addresses.
        bcc (List[str]): Bcc recipients.
        cc (List[str]): Cc recipients.
        received_for (List[str]): Addresses the email was received for.
        message_id (str): RFC Message-ID header value for the email.
        subject (str): Email subject line.
        attachments (List[ReceivedEmailAttachment]): Attachment metadata.
    """

    email_id: str
    """
    Unique identifier for the specific email.
    """
    created_at: str
    """
    ISO 8601 timestamp when the email was received.
    """
    to: List[str]
    """
    Recipient email addresses.
    """
    bcc: List[str]
    """
    Bcc recipients.
    """
    cc: List[str]
    """
    Cc recipients.
    """
    received_for: List[str]
    """
    Addresses the email was received for.
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
    Attachment metadata.
    """


class ContactEventData(TypedDict):
    """
    Data payload for contact webhook events.

    Attributes:
        id (str): The contact ID.
        audience_id (str): The audience ID.
        segment_ids (List[str]): Segment IDs the contact belongs to.
        created_at (str): ISO 8601 timestamp when the contact was created.
        updated_at (str): ISO 8601 timestamp when the contact was last updated.
        email (str): The contact's email address.
        unsubscribed (bool): Whether the contact is unsubscribed.
        first_name (NotRequired[str]): The contact's first name.
        last_name (NotRequired[str]): The contact's last name.
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
    Segment IDs the contact belongs to.
    """
    created_at: str
    """
    ISO 8601 timestamp when the contact was created.
    """
    updated_at: str
    """
    ISO 8601 timestamp when the contact was last updated.
    """
    email: str
    """
    The contact's email address.
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
    DNS record for a domain.

    Attributes:
        record (str): The record identifier.
        name (str): The record name.
        type (str): The record type.
        ttl (str): The record TTL.
        status (str): The record status.
        value (str): The record value.
        priority (NotRequired[int]): The record priority.
    """

    record: str
    """
    The record identifier.
    """
    name: str
    """
    The record name.
    """
    type: str
    """
    The record type.
    """
    ttl: str
    """
    The record TTL.
    """
    status: str
    """
    The record status.
    """
    value: str
    """
    The record value.
    """
    priority: NotRequired[int]
    """
    The record priority.
    """


class DomainEventData(TypedDict):
    """
    Data payload for domain webhook events.

    Attributes:
        id (str): The domain ID.
        name (str): The domain name.
        status (str): The domain status.
        created_at (str): ISO 8601 timestamp when the domain was created.
        region (str): The domain region.
        records (List[DomainRecord]): DNS records for the domain.
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
    ISO 8601 timestamp when the domain was created.
    """
    region: str
    """
    The domain region.
    """
    records: List[DomainRecord]
    """
    DNS records for the domain.
    """


class EmailBouncedEventData(BaseEmailEventData):
    bounce: EmailBounce
    """
    Bounce details from the receiving server.
    """


class EmailClickedEventData(BaseEmailEventData):
    click: EmailClick
    """
    Click tracking details.
    """


class EmailFailedEventData(BaseEmailEventData):
    failed: EmailFailed
    """
    Failure details for the email.
    """


class EmailSuppressedEventData(BaseEmailEventData):
    suppressed: EmailSuppressed
    """
    Suppression details for the email.
    """


class EmailSentEvent(TypedDict):
    """
    Webhook payload for email.sent events.
    """

    type: Literal["email.sent"]
    created_at: str
    data: BaseEmailEventData


class EmailScheduledEvent(TypedDict):
    """
    Webhook payload for email.scheduled events.
    """

    type: Literal["email.scheduled"]
    created_at: str
    data: BaseEmailEventData


class EmailDeliveredEvent(TypedDict):
    """
    Webhook payload for email.delivered events.
    """

    type: Literal["email.delivered"]
    created_at: str
    data: BaseEmailEventData


class EmailDeliveryDelayedEvent(TypedDict):
    """
    Webhook payload for email.delivery_delayed events.
    """

    type: Literal["email.delivery_delayed"]
    created_at: str
    data: BaseEmailEventData


class EmailComplainedEvent(TypedDict):
    """
    Webhook payload for email.complained events.
    """

    type: Literal["email.complained"]
    created_at: str
    data: BaseEmailEventData


class EmailBouncedEvent(TypedDict):
    """
    Webhook payload for email.bounced events.
    """

    type: Literal["email.bounced"]
    created_at: str
    data: EmailBouncedEventData


class EmailOpenedEvent(TypedDict):
    """
    Webhook payload for email.opened events.
    """

    type: Literal["email.opened"]
    created_at: str
    data: BaseEmailEventData


class EmailClickedEvent(TypedDict):
    """
    Webhook payload for email.clicked events.
    """

    type: Literal["email.clicked"]
    created_at: str
    data: EmailClickedEventData


class EmailReceivedEvent(TypedDict):
    """
    Webhook payload for email.received events.
    """

    type: Literal["email.received"]
    created_at: str
    data: ReceivedEmailEventData


class EmailFailedEvent(TypedDict):
    """
    Webhook payload for email.failed events.
    """

    type: Literal["email.failed"]
    created_at: str
    data: EmailFailedEventData


class EmailSuppressedEvent(TypedDict):
    """
    Webhook payload for email.suppressed events.
    """

    type: Literal["email.suppressed"]
    created_at: str
    data: EmailSuppressedEventData


class ContactCreatedEvent(TypedDict):
    """
    Webhook payload for contact.created events.
    """

    type: Literal["contact.created"]
    created_at: str
    data: ContactEventData


class ContactUpdatedEvent(TypedDict):
    """
    Webhook payload for contact.updated events.
    """

    type: Literal["contact.updated"]
    created_at: str
    data: ContactEventData


class ContactDeletedEvent(TypedDict):
    """
    Webhook payload for contact.deleted events.
    """

    type: Literal["contact.deleted"]
    created_at: str
    data: ContactEventData


class DomainCreatedEvent(TypedDict):
    """
    Webhook payload for domain.created events.
    """

    type: Literal["domain.created"]
    created_at: str
    data: DomainEventData


class DomainUpdatedEvent(TypedDict):
    """
    Webhook payload for domain.updated events.
    """

    type: Literal["domain.updated"]
    created_at: str
    data: DomainEventData


class DomainDeletedEvent(TypedDict):
    """
    Webhook payload for domain.deleted events.
    """

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
Union of all webhook event payload types returned by Webhooks.verify.
"""
