from typing import Dict, Union

from typing_extensions import NotRequired, TypedDict


class ContactPropertyValue(TypedDict):
    value: Union[str, int, float, bool]
    """
    The property value, a string, number, or boolean depending on type.
    """
    type: str
    """
    The property type ("string", "number", or "boolean").
    """


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
    properties: NotRequired[Dict[str, ContactPropertyValue]]
    """
    Custom properties for the contact. Only available for global contacts.
    """
