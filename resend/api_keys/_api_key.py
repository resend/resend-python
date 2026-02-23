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
