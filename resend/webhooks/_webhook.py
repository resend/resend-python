from typing import List, Union

from typing_extensions import Literal, TypedDict

WebhookStatus = Literal["enabled", "disabled"]

WebhookEvent = Literal[
    # Email events
    "email.sent",
    "email.delivered",
    "email.delivery_delayed",
    "email.complained",
    "email.bounced",
    "email.opened",
    "email.clicked",
    "email.received",
    "email.failed",
    # Contact events
    "contact.created",
    "contact.updated",
    "contact.deleted",
    # Domain events
    "domain.created",
    "domain.updated",
    "domain.deleted",
]


class Webhook(TypedDict):
    """
    Webhook represents a webhook configuration object

    Attributes:
        id (str): The webhook ID
        object (str): The object type, always "webhook"
        created_at (str): When the webhook was created
        status (str): The webhook status, either "enabled" or "disabled"
        endpoint (str): The URL where webhook events will be sent
        events (List[str]): Array of event types to subscribe to
        signing_secret (Union[str, None]): The signing secret for webhook verification
    """

    id: str
    """
    The webhook ID
    """
    object: str
    """
    The object type, always "webhook"
    """
    created_at: str
    """
    When the webhook was created (ISO 8601 format)
    """
    status: WebhookStatus
    """
    The webhook status, either "enabled" or "disabled"
    """
    endpoint: str
    """
    The URL where webhook events will be sent
    """
    events: List[WebhookEvent]
    """
    Array of event types to subscribe to
    """
    signing_secret: Union[str, None]
    """
    The signing secret for webhook verification
    """
