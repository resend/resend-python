"""Base response type for all Resend API responses."""

from typing import Dict

from typing_extensions import NotRequired, TypedDict


class BaseResponse(TypedDict):
    """Base response type that all API responses inherit from.

    Attributes:
        headers: HTTP response headers including rate limit info, request IDs, etc.
                 Optional field that may not be present in all responses.
    """

    headers: NotRequired[Dict[str, str]]
