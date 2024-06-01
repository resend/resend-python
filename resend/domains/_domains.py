from typing import Any, Dict, List, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.domains._domain import Domain, DomainObject, ShortDomain
from resend.domains._record import Record


class _ListResponse(TypedDict):
    data: List[ShortDomain]
    """
    A list of domain objects
    """


class _CreateResponse(ShortDomain):
    records: Union[List[Record], None]
    """
    The list of domain records
    """
    dnsProvider: str
    """
    The domain DNS provider
    """


class _VerifyResponse(TypedDict):
    object: DomainObject
    """
    The object type
    """
    id: str
    """
    The domain ID
    """


class _UpdateResponse(_VerifyResponse):
    pass


class _RemoveResponse(_VerifyResponse):
    deleted: bool
    """
    The domain deletion status
    """


class Domains:

    class CreateResponse(_CreateResponse):
        """
        CreateResponse type that wraps a domain object

        Attributes:
            id (str): The domain ID
            name (str): The domain name
            created_at (str): When domain was created
            status (str): Status of the domain: not_started, etc..
            region (str): The region where emails will be sent from. Possible values: us-east-1' | 'eu-west-1' | 'sa-east-1' | 'ap-northeast-1'
            records (List[Record]): The list of domain records
            dnsProvider (str): The domain DNS provider
        """

    class ListResponse(_ListResponse):
        """
        ListResponse type that wraps a list of domain objects

        Attributes:
            data (List[ShortDomain]): A list of domain objects
        """

    class RemoveResponse(_RemoveResponse):
        """
        RemoveResponse type that wraps a domain object

        Attributes:
            object (str): The object type
            id (str): The domain ID
            deleted (bool): The domain deletion status
        """

    class VerifyResponse(_VerifyResponse):
        """
        VerifyResponse type that wraps a domain object

        Attributes:
            object (str): The object type
            id (str): The domain ID
        """

    class UpdateResponse(_UpdateResponse):
        """
        UpdateResponse type that wraps a domain object

        Attributes:
            object (str): The object type
            id (str): The domain ID
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
    def create(cls, params: CreateParams) -> CreateResponse:
        """
        Create a domain through the Resend Email API.
        see more: https://resend.com/docs/api-reference/domains/create-domain

        Args:
            params (CreateParams): The domain creation parameters

        Returns:
            Domain: The new domain object
        """
        path = "/domains"
        resp = request.Request[_CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update an existing domain.
        see more: https://resend.com/docs/api-reference/domains/update-domain

        Args:
            params (UpdateParams): The domain update parameters

        Returns:
            Domain: The updated domain object
        """
        path = f"/domains/{params['id']}"
        resp = request.Request[_UpdateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

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
        resp = request.Request[Domain](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls) -> ListResponse:
        """
        Retrieve a list of domains for the authenticated user.
        see more: https://resend.com/docs/api-reference/domains/list-domains

        Returns:
            ListResponse: A list of domain objects
        """
        path = "/domains"
        resp = request.Request[_ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, domain_id: str) -> RemoveResponse:
        """
        Remove an existing domain.
        see more: https://resend.com/docs/api-reference/domains/delete-domain

        Args:
            domain_id (str): The domain ID

        Returns:
            Domain: The removed domain object
        """
        path = f"/domains/{domain_id}"
        resp = request.Request[_RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    def verify(cls, domain_id: str) -> VerifyResponse:
        """
        Verify an existing domain.
        see more: https://resend.com/docs/api-reference/domains/verify-domain

        Args:
            domain_id (str): The domain ID

        Returns:
            Domain: The verified domain object
        """
        path = f"/domains/{domain_id}/verify"
        resp = request.Request[_VerifyResponse](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp
