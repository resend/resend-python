from typing import Dict, Optional, cast, Any
from typing_extensions import TypedDict

from resend import request
from resend.api_keys._api_key import ApiKey


class ApiKeys:
    """
    Api Keys module
    """
    class CreateApiKeyRequestParams(TypedDict):
        name: str
        """
        The API key name.
        """
        permission: Optional[str]
        """
        The API key can have full access to Resend's API or be only
        restricted to send emails. * full_access: Can create, delete, get,
        and update any resource. * sending_access: Can only send emails.
        """
        domain_id: Optional[str]
        """
        Restrict an API key to send emails only from a specific domain.
        This is only used when the permission is set to sending_access.
        """


    @classmethod
    def create(cls, params: "CreateApiKeyRequestParams") -> ApiKey:
        """
        Add a new API key to authenticate communications with Resend.
        see more: https://resend.com/docs/api-reference/api-keys/create-api-key
        """
        path = "/api-keys"
        return ApiKey.create(
            request.Request(
                path=path,
                params=cast(Dict[Any, Any],
                            params),
                verb="post")
                .perform())

    # @classmethod
    # # https://resend.com/docs/api-reference/api-keys/list-api-keys
    # def list(cls) -> Dict:
    #     path = "/api-keys"
    #     return request.Request(path=path, params={}, verb="get").perform()

    # @classmethod
    # # https://resend.com/docs/api-reference/api-keys/delete-api-key
    # def remove(cls, api_key_id="") -> Dict:
    #     path = f"/api-keys/{api_key_id}"
    #     return request.Request(path=path, params={}, verb="delete").perform()
