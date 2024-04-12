class ApiKey:
    id: str
    """
    The api key ID
    """
    token: str
    """
    The api key token
    """
    name: str
    """
    The api key token
    """
    created_at: str
    """
    Api key creation date
    """

    def __init__(self, id: str, token: str, name: str, created_at: str):
        self.id = id
        self.token = token
        self.name = name
        self.created_at = created_at

    @staticmethod
    def new_from_request(val) -> "ApiKey":
        return ApiKey(
            id=val["id"],
            token=val["token"] if "token" in val else None,
            name=val["name"] if "name" in val else None,
            created_at=val["created_at"] if "created_at" in val else None,
            )
