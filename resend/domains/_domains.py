from typing import Any, Dict, List, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.domains._domain import Domain


class _ListResponse(TypedDict):
    data: List[Domain]
    """
    A list of domain objects
    """


class Domains:

    class ListResponse(_ListResponse):
        """
        ListResponse type that wraps a list of domain objects

        Attributes:
            data (List[Domain]): A list of domain objects
        """

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

        Args:
            params (CreateParams): The domain creation parameters

        Returns:
            Domain: The new domain object
        """
        path = "/domains"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform()
        return cast(Domain, resp)

    @classmethod
    def update(cls, params: UpdateParams) -> Domain:
        """
        Update an existing domain.
        see more: https://resend.com/docs/api-reference/domains/update-domain

        Args:
            params (UpdateParams): The domain update parameters

        Returns:
            Domain: The updated domain object
        """
        path = f"/domains/{params['id']}"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform()
        return cast(Domain, resp)

    @classmethod
    def get(cls, domain_id: str) -> Domain:
        """
        Retrieve a single domain for the authenticated user.
        see more: https://resend.com/docs/api-reference/domains/get-domain

        Args:
            domain_id (str): The domain ID

        Returns:
            Domain: The domain object
        """
        path = f"/domains/{domain_id}"
        resp = request.Request(path=path, params={}, verb="get").perform()
        return cast(Domain, resp)

    @classmethod
    def list(cls) -> ListResponse:
        """
        Retrieve a list of domains for the authenticated user.
        see more: https://resend.com/docs/api-reference/domains/list-domains

        Returns:
            ListResponse: A list of domain objects
        """
        path = "/domains"
        resp = request.Request(path=path, params={}, verb="get").perform()
        return cast(_ListResponse, resp)

    @classmethod
    def remove(cls, domain_id: str) -> Domain:
        """
        Remove an existing domain.
        see more: https://resend.com/docs/api-reference/domains/delete-domain

        Args:
            domain_id (str): The domain ID

        Returns:
            Domain: The removed domain object
        """
        path = f"/domains/{domain_id}"
        resp = request.Request(path=path, params={}, verb="delete").perform()
        return cast(Domain, resp)

    @classmethod
    def verify(cls, domain_id: str) -> Domain:
        """
        Verify an existing domain.
        see more: https://resend.com/docs/api-reference/domains/verify-domain

        Args:
            domain_id (str): The domain ID

        Returns:
            Domain: The verified domain object
        """
        path = f"/domains/{domain_id}/verify"
        resp = request.Request(path=path, params={}, verb="post").perform()
        return cast(Domain, resp)
