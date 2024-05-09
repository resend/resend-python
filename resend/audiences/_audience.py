from typing import Any, Dict


class Audience:
    id: str
    """
    The unique identifier of the audience.
    """
    name: str
    """
    The name of the audience.
    """
    created_at: str
    """
    The date and time the audience was created.
    """
    deleted: bool
    """
    Wether the audience was deleted. Only returned on the "remove" call
    """

    def __init__(self, id: str, name: str, created_at: str, deleted: bool = False):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.deleted = deleted

    @staticmethod
    def new_from_request(val: Dict[Any, Any]) -> "Audience":
        """Creates a new Audience object from the
        JSON response from the API.

        Args:
            val (Dict): The JSON response from the API

        Returns:
            Audience: The new Audience object
        """
        audience = Audience(
            id=val["id"] if "id" in val else None,
            name=val["name"] if "name" in val else None,
            created_at=val["created_at"] if "created_at" in val else None,
            deleted=val["deleted"] if "deleted" in val else False,
        )
        return audience
