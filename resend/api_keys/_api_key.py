from typing import Any, Dict
from typing_extensions import TypedDict


class ApiKey(TypedDict):
    id: str
    """
    The api key ID
    """
    token: str
    """
    The api key token
    """
    name: str
    """
    The api key token
    """
    created_at: str
    """
    Api key creation date
    """