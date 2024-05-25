from typing_extensions import TypedDict


class Contact(TypedDict):
    id: str
    """
    The contact id.
    """
    email: str
    """
    The email of the contact.
    """
    first_name: str
    """
    The first name of the contact.
    """
    last_name: str
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
    deleted: bool
    """
    Wether the contact is deleted or not.
    """
