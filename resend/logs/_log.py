from typing import Any

from typing_extensions import NotRequired, TypedDict


class Log(TypedDict):
    id: str
    """
    The log ID
    """
    created_at: str
    """
    The date and time the log was created
    """
    endpoint: str
    """
    The API endpoint that was called
    """
    method: str
    """
    The HTTP method used
    """
    response_status: int
    """
    The HTTP response status code
    """
    user_agent: str
    """
    The user agent of the client
    """
    request_body: NotRequired[Any]
    """
    The original request body (only present when retrieving a single log)
    """
    response_body: NotRequired[Any]
    """
    The API response body (only present when retrieving a single log)
    """
