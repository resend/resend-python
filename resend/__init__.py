import os

from .api_keys._api_key import ApiKey
from .api_keys._api_keys import ApiKeys
from .audiences._audience import Audience
from .audiences._audiences import Audiences
from .broadcasts._broadcast import Broadcast
from .broadcasts._broadcasts import Broadcasts
from .contact_properties._contact_property import ContactProperty
from .contact_properties._contact_properties import ContactProperties
from .contacts._contact import Contact
from .contacts._contact_topic import ContactTopic, TopicSubscriptionUpdate
from .contacts._contacts import Contacts
from .contacts._topics import Topics as ContactsTopics
from .domains._domain import Domain
from .domains._domains import Domains
from .emails._attachment import Attachment, RemoteAttachment
from .emails._attachments import Attachments as EmailAttachments
from .emails._batch import Batch, BatchValidationError
from .emails._email import Email
from .emails._emails import Emails, EmailTemplate
from .emails._received_email import (EmailAttachment, EmailAttachmentDetails,
                                     ListReceivedEmail, ReceivedEmail)
from .emails._receiving import Receiving as EmailsReceiving
from .emails._tag import Tag
from .http_client import HTTPClient
from .http_client_requests import RequestsClient
from .request import Request
from .templates._template import Template, TemplateListItem, Variable
from .templates._templates import Templates
from .topics._topic import Topic
from .topics._topics import Topics
from .version import __version__, get_version
from .webhooks._webhook import (VerifyWebhookOptions, Webhook, WebhookEvent,
                                WebhookHeaders, WebhookStatus)
from .webhooks._webhooks import Webhooks

# Config vars
api_key = os.environ.get("RESEND_API_KEY")
api_url = os.environ.get("RESEND_API_URL", "https://api.resend.com")

# HTTP Client
default_http_client: HTTPClient = RequestsClient()

__all__ = [
    "__version__",
    "get_version",
    "Request",
    "Emails",
    "ApiKeys",
    "Domains",
    "Batch",
    "Audiences",
    "Contacts",
    "ContactProperties",
    "Broadcasts",
    "Templates",
    "Webhooks",
    "Topics",
    # Types
    "Audience",
    "Contact",
    "ContactProperty",
    "ContactTopic",
    "TopicSubscriptionUpdate",
    "Domain",
    "ApiKey",
    "Email",
    "Attachment",
    "RemoteAttachment",
    "EmailTemplate",
    "Tag",
    "Broadcast",
    "Template",
    "TemplateListItem",
    "Variable",
    "Webhook",
    "WebhookEvent",
    "WebhookHeaders",
    "WebhookStatus",
    "VerifyWebhookOptions",
    "Topic",
    "BatchValidationError",
    "ReceivedEmail",
    "EmailAttachment",
    "EmailAttachmentDetails",
    "ListReceivedEmail",
    # Receiving types (for type hints)
    "EmailsReceiving",
    "EmailAttachments",
    "ContactsTopics",
    # Default HTTP Client
    "RequestsClient",
]
