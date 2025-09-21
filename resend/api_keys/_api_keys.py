from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.api_keys._api_key import ApiKey
from resend.pagination_helper import PaginationHelper


class ApiKeys:

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of API key objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[ApiKey]): A list of API key objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[ApiKey]
        """
        A list of API key objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class CreateApiKeyResponse(TypedDict):
        """
        CreateApiKeyResponse is the type that wraps the response of the API key that was created

        Attributes:
            id (str): The ID of the created API key
            token (str): The token of the created API key
        """

        id: str
        """
        The ID of the created API key
        """
        token: str
        """
        The token of the created API key
        """

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of API keys to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more API keys (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more API keys (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class CreateParams(TypedDict):
        name: str
        """
        The API key name.
        """
        permission: NotRequired[str]
        """
        The API key can have full access to Resend's API or be only
        restricted to send emails. * full_access: Can create, delete, get,
        and update any resource. * sending_access: Can only send emails.
        """
        domain_id: NotRequired[str]
        """
        Restrict an API key to send emails only from a specific domain.
        This is only used when the permission is set to sending_access.
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateApiKeyResponse:
        """
        Add a new API key to authenticate communications with Resend.
        see more: https://resend.com/docs/api-reference/api-keys/create-api-key

        Args:
            params (CreateParams): The API key creation parameters

        Returns:
            CreateApiKeyResponse: The created API key response with id and token
        """
        path = "/api-keys"
        resp = request.Request[ApiKeys.CreateApiKeyResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of API keys for the authenticated user.
        see more: https://resend.com/docs/api-reference/api-keys/list-api-keys

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of API keys to retrieve (max 100, min 1)
                - after: ID after which to retrieve more API keys
                - before: ID before which to retrieve more API keys

        Returns:
            ListResponse: A list of API key objects
        """
        base_path = "/api-keys"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[ApiKeys.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, api_key_id: str) -> None:
        """
        Remove an existing API key.
        see more: https://resend.com/docs/api-reference/api-keys/delete-api-key

        Args:
            api_key_id (str): The ID of the API key to remove

        Returns:
            None
        """
        path = f"/api-keys/{api_key_id}"

        # This would raise if failed
        request.Request[None](path=path, params={}, verb="delete").perform()
        return None
