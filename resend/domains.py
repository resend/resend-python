from typing import Dict

from resend import request


class Domains:
    """Domains API Wrapper"""

    @classmethod
    # https://resend.com/docs/api-reference/domains/create-domain
    def create(cls, params={}) -> Dict:
        path = "/domains"
        return request.Request(path=path, params=params, verb="post").perform()

    @classmethod
    # https://resend.com/docs/api-reference/domains/update-domain
    def update(cls, params={}) -> Dict:
        path = f"/domains/{params['id']}"
        return request.Request(path=path, params=params, verb="patch").perform()

    @classmethod
    # https://resend.com/docs/api-reference/domains/get-domain
    def get(cls, domain_id="") -> Dict:
        path = f"/domains/{domain_id}"
        return request.Request(path=path, params={}, verb="get").perform()

    @classmethod
    # https://resend.com/docs/api-reference/domains/list-domains
    def list(cls) -> Dict:
        path = "/domains"
        return request.Request(path=path, params={}, verb="get").perform()

    @classmethod
    # https://resend.com/docs/api-reference/domains/delete-domain
    def remove(cls, domain_id="") -> Dict:
        path = f"/domains/{domain_id}"
        return request.Request(path=path, params={}, verb="delete").perform()

    @classmethod
    # https://resend.com/docs/api-reference/domains/verify-domain
    def verify(cls, domain_id="") -> Dict:
        path = f"/domains/{domain_id}/verify"
        return request.Request(path=path, params={}, verb="post").perform()
