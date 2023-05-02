from typing import Dict

from resend import request


class ApiKeys:
    """Api Keys API Wrapper"""

    @classmethod
    # https://resend.com/docs/api-reference/api-keys/create-api-key
    def create(cls, params={}) -> Dict:
        path = "/api-keys"
        return request.Request(path=path, params=params, verb="post").perform()

    @classmethod
    # https://resend.com/docs/api-reference/api-keys/list-api-keys
    def list(cls) -> Dict:
        path = "/api-keys"
        return request.Request(path=path, params={}, verb="get").perform()

    @classmethod
    # https://resend.com/docs/api-reference/api-keys/delete-api-key
    def remove(cls, api_key_id="") -> Dict:
        path = f"/api-keys/{api_key_id}"
        return request.Request(path=path, params={}, verb="delete").perform()
