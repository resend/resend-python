import os

from .api_keys._api_keys import ApiKeys
from .audiences import Audiences
# from .batch import Batch
from .contacts import Contacts
from .domains._domains import Domains
from .emails._emails import Emails
from .request import Request
from .version import get_version

# Config vars
api_key: str | None = os.environ.get("RESEND_API_KEY")
api_url: str | None = os.environ.get("RESEND_API_URL", "https://api.resend.com")

# API resources
from .emails._emails import Emails  # noqa

__all__ = [
    "get_version",
    "Request",
    "Emails",
    "ApiKeys",
    "Domains",
    "Batch",
    "Audiences",
    "Contacts",
]
