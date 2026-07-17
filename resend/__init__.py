import os
from typing import Optional, Union

from .api_keys._api_key import ApiKey
from .api_keys._api_keys import ApiKeys
from .audiences._audience import Audience
from .audiences._audiences import Audiences
from .automations._automation import (Automation, AutomationConnection,
                                      AutomationConnectionType,
                                      AutomationListItem,
                                      AutomationResponseStep, AutomationRun,
                                      AutomationRunListItem,
                                      AutomationRunStatus, AutomationRunStep,
                                      AutomationStatus, AutomationStep,
                                      AutomationStepType)
from .automations._automations import Automations
from .broadcasts._broadcast import Broadcast
from .broadcasts._broadcasts import Broadcasts
from .contact_properties._contact_properties import ContactProperties
from .contact_properties._contact_property import ContactProperty
from .contacts._contact import Contact
from .contacts._contact_topic import ContactTopic, TopicSubscriptionUpdate
from .contacts._contacts import Contacts
from .contacts._topics import Topics as ContactsTopics
from .contacts.imports._contact_import import (ContactImport,
                                               ContactImportCounts)
from .contacts.imports._contact_imports import ContactImports
from .contacts.segments._contact_segment import ContactSegment
from .contacts.segments._contact_segments import ContactSegments
from .domains._domain import Domain
from .domains._domains import Domains
from .domains.claims._domain_claim import DomainClaim, DomainClaimRecord
from .domains.claims._domain_claims import DomainClaims
from .emails._attachment import Attachment, RemoteAttachment
from .emails._attachments import Attachments as EmailAttachments
from .emails._batch import Batch, BatchValidationError
from .emails._email import Email
from .emails._emails import Emails, EmailTemplate
from .emails._received_email import (AttachmentWithSignedUrl, EmailAttachment,
                                     EmailAttachmentDetails, ListReceivedEmail,
                                     ReceivedEmail)
from .emails._receiving import Receiving as EmailsReceiving
from .emails._tag import Tag
from .events._event import (Event, EventListItem, EventSchema,
                            EventSchemaFieldType)
from .events._events import Events
from .http_client import HTTPClient
from .http_client_async import \
    AsyncHTTPClient  # Okay to import AsyncHTTPClient since it is just an interface.
from .http_client_requests import RequestsClient
from .logs._log import Log
from .logs._logs import Logs
from .oauth_grants._oauth_grant import OAuthGrant, OAuthGrantClient
from .oauth_grants._oauth_grants import OAuthGrants
from .request import Request
from .segments._segment import Segment
from .segments._segments import Segments
from .templates._template import Template, TemplateListItem, Variable
from .templates._templates import Templates
from .topics._topic import Topic
from .topics._topics import Topics
from .version import __version__, get_version
from .webhooks._webhook import (VerifyWebhookOptions, Webhook, WebhookEvent,
                                WebhookHeaders, WebhookStatus)
from .webhooks._webhook_event import (BaseEmailEventData, ContactCreatedEvent,
                                      ContactDeletedEvent, ContactEventData,
                                      ContactUpdatedEvent, DomainCreatedEvent,
                                      DomainDeletedEvent, DomainEventData,
                                      DomainUpdatedEvent, EmailBouncedEvent,
                                      EmailClickedEvent, EmailComplainedEvent,
                                      EmailDeliveredEvent,
                                      EmailDeliveryDelayedEvent,
                                      EmailFailedEvent, EmailOpenedEvent,
                                      EmailReceivedEvent, EmailScheduledEvent,
                                      EmailSentEvent, EmailSuppressedEvent,
                                      ReceivedEmailEventData,
                                      WebhookEventPayload)
from .webhooks._webhooks import Webhooks

# Type for clients that support both sync and async
ResendHTTPClient = Union[HTTPClient, AsyncHTTPClient]

# Sync HTTP client — always set, can be overridden with a custom HTTPClient.
default_http_client: ResendHTTPClient = RequestsClient()

# Async HTTP client — auto-detected if httpx is installed, can be overridden
# with any AsyncHTTPClient subclass. Set to None if no async library is available.
default_async_http_client: Optional[AsyncHTTPClient] = None

# Config vars
api_key = os.environ.get("RESEND_API_KEY")
api_url = os.environ.get("RESEND_API_URL", "https://api.resend.com")


__all__ = [
    "__version__",
    "get_version",
    "Request",
    "Emails",
    "ApiKeys",
    "Domains",
    "DomainClaims",
    "Batch",
    "Audiences",
    "Automations",
    "Contacts",
    "ContactImports",
    "ContactProperties",
    "Broadcasts",
    "Events",
    "Segments",
    "Templates",
    "Webhooks",
    "Topics",
    "Logs",
    "OAuthGrants",
    # Types
    "Audience",
    "Automation",
    "AutomationConnection",
    "AutomationConnectionType",
    "AutomationListItem",
    "AutomationResponseStep",
    "AutomationRun",
    "AutomationRunListItem",
    "AutomationRunStatus",
    "AutomationRunStep",
    "AutomationStatus",
    "AutomationStep",
    "AutomationStepType",
    "Event",
    "EventListItem",
    "EventSchema",
    "EventSchemaFieldType",
    "Contact",
    "ContactImport",
    "ContactImportCounts",
    "ContactSegment",
    "ContactSegments",
    "ContactProperty",
    "ContactTopic",
    "TopicSubscriptionUpdate",
    "Domain",
    "DomainClaim",
    "DomainClaimRecord",
    "ApiKey",
    "Log",
    "Email",
    "Attachment",
    "RemoteAttachment",
    "EmailTemplate",
    "Tag",
    "Broadcast",
    "Segment",
    "Template",
    "TemplateListItem",
    "Variable",
    "Webhook",
    "WebhookEvent",
    "WebhookEventPayload",
    "WebhookHeaders",
    "WebhookStatus",
    "VerifyWebhookOptions",
    "BaseEmailEventData",
    "ReceivedEmailEventData",
    "ContactEventData",
    "DomainEventData",
    "EmailSentEvent",
    "EmailScheduledEvent",
    "EmailDeliveredEvent",
    "EmailDeliveryDelayedEvent",
    "EmailComplainedEvent",
    "EmailBouncedEvent",
    "EmailOpenedEvent",
    "EmailClickedEvent",
    "EmailReceivedEvent",
    "EmailFailedEvent",
    "EmailSuppressedEvent",
    "ContactCreatedEvent",
    "ContactUpdatedEvent",
    "ContactDeletedEvent",
    "DomainCreatedEvent",
    "DomainUpdatedEvent",
    "DomainDeletedEvent",
    "Topic",
    "OAuthGrant",
    "OAuthGrantClient",
    "BatchValidationError",
    "ReceivedEmail",
    "EmailAttachment",
    "AttachmentWithSignedUrl",
    "EmailAttachmentDetails",
    "ListReceivedEmail",
    # Receiving types (for type hints)
    "EmailsReceiving",
    "EmailAttachments",
    "ContactsTopics",
    # HTTP Clients
    "HTTPClient",
    # Default HTTP Client
    "RequestsClient",
]

# Add async exports and auto-detect async client if httpx is available
try:
    from .async_request import AsyncRequest  # noqa: F401
    from .http_client_httpx import HTTPXClient  # noqa: F401

    default_async_http_client = HTTPXClient()
    __all__.extend(["AsyncHTTPClient", "HTTPXClient", "AsyncRequest"])
except ImportError:
    pass
