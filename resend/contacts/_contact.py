from typing import Any, Dict

from typing_extensions import NotRequired, TypedDict


class Contact(TypedDict):
    id: str
    """
    The contact id.
    """
    email: str
    """
    The email of the contact.
    """
    first_name: NotRequired[str]
    """
    The first name of the contact.
    """
    last_name: NotRequired[str]
    """
    The last name of the contact.
    """
    created_at: str
    """
    The timestamp of the contact.
    """
    unsubscribed: bool
    """
    The unsubscribed status of the contact.
    """
    properties: NotRequired[Dict[str, Any]]
    """
    Custom properties associated with the contact.
    """
