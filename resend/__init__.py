from .api import Resend
from .emails import Emails
from .request import Request
from .version import get_version

# Config vars
api_key = None

# API resources
from .emails import Emails  # noqa

__all__ = ["get_version", "Resend", "Request", "Emails"]
