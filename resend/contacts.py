from typing import Dict

from resend import request


class Contacts:
    """Contacts API Wrapper"""

    @classmethod
    # https://resend.com/docs/api-reference/contacts/create-contact
    def create(cls, params={}) -> Dict:
        path = f"/audiences/{params['audience_id']}/contacts"
        return request.Request(path=path, params=params, verb="post").perform()

    @classmethod
    # https://resend.com/docs/api-reference/audiences/list-audiences
    def list(cls, audience_id) -> Dict:
        path = f"/audiences/#{audience_id}/contacts"
        return request.Request(path=path, params={}, verb="get").perform()

    @classmethod
    # https://resend.com/docs/api-reference/audiences/get-audience
    def get(cls, audience_id, id) -> Dict:
        path = f"/audiences/{audience_id}/contacts/{id}"
        return request.Request(path=path, params={}, verb="get").perform()

    @classmethod
    # https://resend.com/docs/api-reference/audiences/delete-audience
    def remove(cls, audience_id, id) -> Dict:
        path = f"/audiences/{id}/contacts/{id}"
        return request.Request(path=path, params={}, verb="delete").perform()
