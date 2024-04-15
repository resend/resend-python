class Contact:
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

    def __init__(self, id, email, first_name,
                 last_name, created_at, unsubscribed):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.unsubscribed = unsubscribed

    @staticmethod
    def new_from_request(val) -> "Contact":
        contact = Contact(
            id=val["id"] if "id" in val else "",
            email=val["email"] if "email" in val else "",
            first_name=val["first_name"] if "first_name" in val else "",
            last_name=val["last_name"] if "last_name" in val else "",
            created_at=val["created_at"] if "created_at" in val else "",
            unsubscribed=val["unsubscribed"] if "unsubscribed" in val else False
        )
        return contact
