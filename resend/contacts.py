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
    # https://resend.com/docs/api-reference/contacts/update-contact
    def update(cls, params={}) -> Dict:
        path = f"/audiences/{params['audience_id']}/contacts/{params['id']}"
        return request.Request(path=path, params=params, verb="patch").perform()

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
    def remove(cls, audience_id, id="", email="") -> Dict:
        contact = email if id == "" else id
        if contact == "":
            raise ValueError("id or email must be provided")
        path = f"/audiences/{audience_id}/contacts/{contact}"
        return request.Request(path=path, params={}, verb="delete").perform()
