from typing import Optional

from typing_extensions import TypedDict


class ApiKey(TypedDict):
    id: str
    """
    The API key ID
    """
    name: str
    """
    The API key name
    """
    created_at: str
    """
    The API key creation date
    """
    last_used_at: Optional[str]
    """
    The date and time the API key was last used, or None if never used
    """
