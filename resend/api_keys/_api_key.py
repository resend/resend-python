from typing_extensions import TypedDict


class ApiKey(TypedDict):
    id: str
    """
    The api key ID
    """
    name: str
    """
    The api key token
    """
    created_at: str
    """
    Api key creation date
    """
