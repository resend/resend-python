from typing import Dict

from resend import request


class Audiences:
    """Audiences API Wrapper"""

    @classmethod
    # https://resend.com/docs/api-reference/audiences/create-audience
    def create(cls, params={}) -> Dict:
        path = "/audiences"
        return request.Request(path=path, params=params, verb="post").perform()

    @classmethod
    # https://resend.com/docs/api-reference/audiences/list-audiences
    def list(cls) -> Dict:
        path = "/audiences/"
        return request.Request(path=path, params={}, verb="get").perform()

    @classmethod
    # https://resend.com/docs/api-reference/audiences/get-audience
    def get(cls, id) -> Dict:
        path = f"/audiences/{id}"
        return request.Request(path=path, params={}, verb="get").perform()

    @classmethod
    # https://resend.com/docs/api-reference/audiences/delete-audience
    def remove(cls, id="") -> Dict:
        path = f"/audiences/{id}"
        return request.Request(path=path, params={}, verb="delete").perform()
