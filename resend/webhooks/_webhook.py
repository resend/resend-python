from typing import List, Union

from typing_extensions import TypedDict

from resend.webhooks._webhooks import WebhookStatus


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
    events: List[str]
    """
    Array of event types to subscribe to
    """
    signing_secret: Union[str, None]
    """
    The signing secret for webhook verification
    """
