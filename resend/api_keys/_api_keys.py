from typing import Any, Dict, List, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.api_keys._api_key import ApiKey


class ApiKeys:
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
    def create(cls, params: CreateParams) -> ApiKey:
        """
        Add a new API key to authenticate communications with Resend.
        see more: https://resend.com/docs/api-reference/api-keys/create-api-key

        Args:
            params (CreateParams): The API key creation parameters

        Returns:
            ApiKey: The new API key object
        """
        path = "/api-keys"
        return ApiKey.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params), verb="post"
            ).perform()
        )

    @classmethod
    def list(cls) -> List[ApiKey]:
        """
        Retrieve a list of API keys for the authenticated user.
        see more: https://resend.com/docs/api-reference/api-keys/list-api-keys

        Returns:
            List[ApiKey]: A list of API key objects
        """
        path = "/api-keys"
        resp = request.Request(path=path, params={}, verb="get").perform()
        return [ApiKey.new_from_request(val) for val in resp["data"]]

    @classmethod
    def remove(cls, api_key_id: str = "") -> None:
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
        request.Request(path=path, params={}, verb="delete").perform()
        return None
