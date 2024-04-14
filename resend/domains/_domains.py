from typing import List, Any, Dict, cast

from typing_extensions import TypedDict, NotRequired
from resend import request
from resend.domains._domain import Domain

class Domains:

    class UpdateParams(TypedDict):
        id: str
        """
        The domain ID.
        """
        click_tracking: NotRequired[bool]
        """
        Track clicks within the body of each HTML email.
        """
        open_tracking: NotRequired[bool]
        """
        Track the open rate of each email.
        """

    class CreateParams(TypedDict):
        name: str
        """
        The domain name.
        """
        region: NotRequired[str]
        """
        The region where emails will be sent from.
        Possible values: us-east-1' | 'eu-west-1' | 'sa-east-1' | 'ap-northeast-1'
        """

    @classmethod
    def create(cls, params: CreateParams) -> Domain:
        """
        Create a domain through the Resend Email API.
        see more: https://resend.com/docs/api-reference/domains/create-domain
        """
        path = "/domains"
        return Domain.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params), verb="post"
            ).perform()
        )

    @classmethod
    def update(cls, params: UpdateParams) -> Domain:
        """
        Update an existing domain.
        see more: https://resend.com/docs/api-reference/domains/update-domain
        """
        path = f"/domains/{params['id']}"
        return Domain.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params), verb="patch")
            .perform()
        )

    @classmethod
    def get(cls, domain_id: str = "") -> Domain:
        """
        Retrieve a single domain for the authenticated user.
        see more: https://resend.com/docs/api-reference/domains/get-domain
        """
        path = f"/domains/{domain_id}"
        return Domain.new_from_request(
            request.Request(path=path, params={}, verb="get").perform()
        )

    @classmethod
    def list(cls) -> List[Domain]:
        """
        Retrieve a list of domains for the authenticated user.
        see more: https://resend.com/docs/api-reference/domains/list-domains
        """
        path = "/domains"
        resp = request.Request(path=path, params={}, verb="get").perform()
        return [Domain.new_from_request(val) for val in resp['data']]

    @classmethod
    def remove(cls, domain_id: str = "") -> Domain:
        """
        Remove an existing domain.
        see more: https://resend.com/docs/api-reference/domains/remove-domain
        """
        path = f"/domains/{domain_id}"
        return Domain.new_from_request(
            request.Request(path=path, params={}, verb="delete").perform()
        )

    @classmethod
    def verify(cls, domain_id: str = "" ) -> Domain:
        """
        Verify an existing domain.
        see more: https://resend.com/docs/api-reference/domains/verify-domain
        """
        path = f"/domains/{domain_id}/verify"
        return Domain.new_from_request(
            request.Request(path=path, params={}, verb="post").perform()
        )
