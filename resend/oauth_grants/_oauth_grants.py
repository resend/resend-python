from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.oauth_grants._oauth_grant import OAuthGrant
from resend.pagination_helper import PaginationHelper

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class OAuthGrants:

    class ListResponse(BaseResponse):
        """
        ListResponse type that wraps a list of OAuth grant objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[OAuthGrant]): A list of OAuth grant objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[OAuthGrant]
        """
        A list of OAuth grant objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class RevokeOAuthGrantResponse(BaseResponse):
        """
        RevokeOAuthGrantResponse is the type that wraps the revoked OAuth grant response.

        Attributes:
            object (str): The object type, always "oauth_grant"
            id (str): The ID of the revoked OAuth grant
            revoked_at (str): The date and time the grant was revoked
            revoked_reason (str): The reason the grant was revoked
        """

        object: str
        """
        The object type, always "oauth_grant"
        """
        id: str
        """
        The ID of the revoked OAuth grant
        """
        revoked_at: str
        """
        The date and time the grant was revoked
        """
        revoked_reason: str
        """
        The reason the grant was revoked
        """

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of OAuth grants to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more OAuth grants (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more OAuth grants (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of OAuth grants for the authenticated user.
        see more: https://resend.com/docs/api-reference/oauth/list-grants

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of OAuth grants to retrieve (max 100, min 1)
                - after: ID after which to retrieve more OAuth grants
                - before: ID before which to retrieve more OAuth grants

        Returns:
            ListResponse: A list of OAuth grant objects
        """
        base_path = "/oauth/grants"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[OAuthGrants.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def revoke(cls, oauth_grant_id: str) -> RevokeOAuthGrantResponse:
        """
        Revoke an existing OAuth grant.
        see more: https://resend.com/docs/api-reference/oauth/revoke-grant

        Args:
            oauth_grant_id (str): The ID of the OAuth grant to revoke

        Returns:
            RevokeOAuthGrantResponse: The revoked OAuth grant response
        """
        path = f"/oauth/grants/{oauth_grant_id}"
        resp = request.Request[OAuthGrants.RevokeOAuthGrantResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of OAuth grants for the authenticated user (async).
        see more: https://resend.com/docs/api-reference/oauth/list-grants

        Args:
            params (Optional[ListParams]): Optional pagination parameters

        Returns:
            ListResponse: A list of OAuth grant objects
        """
        base_path = "/oauth/grants"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = await AsyncRequest[OAuthGrants.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def revoke_async(cls, oauth_grant_id: str) -> RevokeOAuthGrantResponse:
        """
        Revoke an existing OAuth grant (async).
        see more: https://resend.com/docs/api-reference/oauth/revoke-grant

        Args:
            oauth_grant_id (str): The ID of the OAuth grant to revoke

        Returns:
            RevokeOAuthGrantResponse: The revoked OAuth grant response
        """
        path = f"/oauth/grants/{oauth_grant_id}"
        resp = await AsyncRequest[OAuthGrants.RevokeOAuthGrantResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
