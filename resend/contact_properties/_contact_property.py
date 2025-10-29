from typing import Union

from typing_extensions import TypedDict


class ContactProperty(TypedDict):
    """
    ContactProperty represents a custom property definition for contacts.

    Attributes:
        id (str): The unique identifier for the contact property
        key (str): The key name of the property
        object (str): The object type, always "contact_property"
        created_at (str): The ISO 8601 timestamp when the property was created
        type (str): The data type of the property (e.g., "string", "number")
        fallback_value (Union[str, int, float, None]): The default value used when a contact doesn't have this property set
    """

    id: str
    """
    The unique identifier for the contact property.
    """
    key: str
    """
    The key name of the property.
    """
    object: str
    """
    The object type, always "contact_property".
    """
    created_at: str
    """
    The ISO 8601 timestamp when the property was created.
    """
    type: str
    """
    The data type of the property (e.g., "string", "number").
    """
    fallback_value: Union[str, int, float, None]
    """
    The default value used when a contact doesn't have this property set.
    Must match the type of the property (string or number).
    """
