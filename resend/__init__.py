from .api import Resend
from .api_keys import ApiKeys
from .domains import Domains
from .emails import Emails
from .request import Request
from .version import get_version

# Config vars
api_key = None

# API resources
from .emails import Emails  # noqa

__all__ = ["get_version", "Resend", "Request", "Emails", "ApiKeys", "Domains"]
