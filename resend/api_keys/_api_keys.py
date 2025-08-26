from typing import Any, Dict, List, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.api_keys._api_key import ApiKey

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class ApiKeys:

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of API key objects

        Attributes:
            data (List[ApiKey]): A list of API key objects
        """

        data: List[ApiKey]
        """
        A list of API key objects
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
    def list(cls) -> ListResponse:
        """
        Retrieve a list of API keys for the authenticated user.
        see more: https://resend.com/docs/api-reference/api-keys/list-api-keys

        Returns:
            ListResponse: A list of API key objects
        """
        path = "/api-keys"
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

    @classmethod
    async def create_async(cls, params: CreateParams) -> ApiKey:
        """
        Add a new API key to authenticate communications with Resend (async).
        see more: https://resend.com/docs/api-reference/api-keys/create-api-key

        Args:
            params (CreateParams): The API key creation parameters

        Returns:
            ApiKey: The new API key object
        """
        path = "/api-keys"
        resp = await AsyncRequest[ApiKey](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls) -> ListResponse:
        """
        Retrieve a list of API keys for the authenticated user (async).
        see more: https://resend.com/docs/api-reference/api-keys/list-api-keys

        Returns:
            ListResponse: A list of API key objects
        """
        path = "/api-keys"
        resp = await AsyncRequest[_ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, api_key_id: str) -> None:
        """
        Remove an existing API key (async).
        see more: https://resend.com/docs/api-reference/api-keys/delete-api-key

        Args:
            api_key_id (str): The ID of the API key to remove

        Returns:
            None
        """
        path = f"/api-keys/{api_key_id}"

        # This would raise if failed
        await AsyncRequest[None](path=path, params={}, verb="delete").perform()
        return None
