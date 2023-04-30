from .api import Resend
from .version import get_version
from .request import Request
from .emails import Emails

# Config vars
api_key = None

# API resources
from .emails import Emails  # noqa

__all__ = ["get_version", "Resend", "Request", "Emails"]
