import os

from .api_keys._api_key import ApiKey
from .api_keys._api_keys import ApiKeys
from .audiences._audience import Audience
from .audiences._audiences import Audiences
from .broadcasts._broadcast import Broadcast
from .broadcasts._broadcasts import Broadcasts
from .contacts._contact import Contact
from .contacts._contacts import Contacts
from .domains._domain import Domain
from .domains._domains import Domains
from .emails._attachment import Attachment, RemoteAttachment
from .emails._batch import Batch
from .emails._email import Email
from .emails._emails import Emails
from .emails._tag import Tag
from .http_client import HTTPClient
from .http_client_requests import RequestsClient
from .request import Request
from .version import __version__, get_version

# Config vars
api_key = os.environ.get("RESEND_API_KEY")
api_url = os.environ.get("RESEND_API_URL", "https://api.resend.com")

# HTTP Client
default_http_client: HTTPClient = RequestsClient()

# API resources
from .emails._emails import Emails  # noqa

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
    "Broadcasts",
    # Types
    "Audience",
    "Contact",
    "Domain",
    "ApiKey",
    "Email",
    "Attachment",
    "RemoteAttachment",
    "Tag",
    "Broadcast",
    # Default HTTP Client
    "RequestsClient",
]
