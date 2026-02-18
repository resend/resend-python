from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import Literal, NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.domains._domain import Domain
from resend.domains._record import Record
from resend.pagination_helper import PaginationHelper

TlsOptions = Literal["enforced", "opportunistic"]


class Domains:

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of domains to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more domains (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more domains (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse type that wraps a list of domain objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[Domain]): A list of domain objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[Domain]
        """
        A list of domain objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class CreateDomainResponse(BaseResponse):
        """
        CreateDomainResponse is the type that wraps the response of the domain that was created

        Attributes:
            id (str): The ID of the created domain
            name (str): The name of the created domain
            created_at (str): When the domain was created
            status (str): Status of the domain
            region (str): The region where emails will be sent from
            records (Union[List[Record], None]): The list of domain records
        """

        id: str
        """
        The ID of the created domain
        """
        name: str
        """
        The name of the created domain
        """
        created_at: str
        """
        When the domain was created
        """
        status: str
        """
        Status of the domain
        """
        region: str
        """
        The region where emails will be sent from
        """
        records: Union[List[Record], None]
        """
        The list of domain records
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
        tls: NotRequired[TlsOptions]
        """
        default: "opportunistic"
        opportunistic: Opportunistic TLS means that it always attempts to make a
        secure connection to the receiving mail server.
        If it can't establish a secure connection, it sends the message unencrypted.

        enforced: Enforced TLS on the other hand, requires that the email
        communication must use TLS no matter what.
        If the receiving server does not support TLS, the email will not be sent.
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
        custom_return_path: NotRequired[str]
        """
        By default, Resend will use the `send` subdomain for the Return-Path address.
        You can change this by setting the optional `custom_return_path` parameter
        when creating a domain via the API or under Advanced options in the dashboard.
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateDomainResponse:
        """
        Create a domain through the Resend Email API.
        see more: https://resend.com/docs/api-reference/domains/create-domain

        Args:
            params (CreateParams): The domain creation parameters

        Returns:
            CreateDomainResponse: The created domain response
        """
        path = "/domains"
        resp = request.Request[Domains.CreateDomainResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

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
        resp = request.Request[Domain](
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
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of domains for the authenticated user.
        see more: https://resend.com/docs/api-reference/domains/list-domains

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of domains to retrieve (max 100, min 1).
                  If not provided, all domains will be returned without pagination.
                - after: ID after which to retrieve more domains
                - before: ID before which to retrieve more domains

        Returns:
            ListResponse: A list of domain objects
        """
        base_path = "/domains"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Domains.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

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
        resp = request.Request[Domain](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

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
        resp = request.Request[Domain](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp
