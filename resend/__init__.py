import os

from .api import Resend
from .api_keys import ApiKeys
from .domains import Domains
from .emails import Emails
from .batch import Batch
from .request import Request
from .version import get_version

# Config vars
api_key = os.environ.get("RESEND_API_KEY")
api_url = os.environ.get("RESEND_API_URL", "https://api.resend.com")

# API resources
from .emails import Emails  # noqa

__all__ = ["get_version", "Resend", "Request", "Emails", "ApiKeys", "Domains", "Batch"]
