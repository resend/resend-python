from typing import Any, Dict, Optional

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
    first_name: Optional[str]
    """
    The first name of the contact. None when the contact has no first name.
    """
    last_name: Optional[str]
    """
    The last name of the contact. None when the contact has no last name.
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
    Custom properties for the contact. Only available for global contacts.
    """
