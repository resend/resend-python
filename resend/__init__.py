import os
from typing import Union

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
from .emails._attachment import Attachment
from .emails._batch import Batch
from .emails._email import Email
from .emails._emails import Emails
from .emails._tag import Tag
from .http_client import HTTPClient
from .http_client_async import \
    AsyncHTTPClient  # Okay to import AsyncHTTPClient since it is just an interface.
from .http_client_requests import RequestsClient
from .request import Request
from .version import __version__, get_version

# Type for clients that support both sync and async
ResendHTTPClient = Union[HTTPClient, AsyncHTTPClient]

# This is the client that is set by default HTTP Client
# But this can be overridden by the user and set to an async client.
default_http_client: ResendHTTPClient = RequestsClient()


# Config vars
api_key = os.environ.get("RESEND_API_KEY")
api_url = os.environ.get("RESEND_API_URL", "https://api.resend.com")


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
    "Tag",
    "Broadcast",
    # HTTP Clients
    "HTTPClient",
    # Default HTTP Client
    "RequestsClient",
]

# Add async exports if available
try:
    from .async_request import AsyncRequest  # noqa: F401
    from .http_client_httpx import HTTPXClient  # noqa: F401

    __all__.extend(["AsyncHTTPClient", "HTTPXClient", "AsyncRequest"])
except ImportError:
    pass
