class ApiKey:
    id: str
    """
    The api key ID
    """
    token: str
    """
    The api key token
    """

    def __init__(self, id: str, token: str):
        self.id = id
        self.token = token

    @staticmethod
    def create(val) -> "ApiKey":
        return ApiKey(id=val["id"], token=val["token"])