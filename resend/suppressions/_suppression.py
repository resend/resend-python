from typing import Optional

from typing_extensions import Literal, TypedDict

from resend._base_response import BaseResponse

SuppressionOrigin = Literal[
    "bounce",
    "complaint",
    "manual",
]


class SuppressionListItem(TypedDict):
    """
    SuppressionListItem represents a suppression in list responses.

    List entries do not carry the 'object' field that the get response includes.

    Attributes:
        id (str): The ID of the suppression.
        email (str): The suppressed email address.
        origin (SuppressionOrigin): What caused the address to be suppressed.
        source_id (Optional[str]): The ID of the event that caused the suppression,
            such as the email that bounced or complained. None for manual suppressions.
        created_at (str): The date and time the suppression was created.
    """

    id: str
    email: str
    origin: SuppressionOrigin
    source_id: Optional[str]
    created_at: str


class Suppression(BaseResponse):
    """
    Suppression represents an email address that Resend will not deliver to.

    Attributes:
        object (str): Always 'suppression'.
        id (str): The ID of the suppression.
        email (str): The suppressed email address.
        origin (SuppressionOrigin): What caused the address to be suppressed.
        source_id (Optional[str]): The ID of the event that caused the suppression,
            such as the email that bounced or complained. None for manual suppressions.
        created_at (str): The date and time the suppression was created.
    """

    object: str
    id: str
    email: str
    origin: SuppressionOrigin
    source_id: Optional[str]
    created_at: str
