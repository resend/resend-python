from typing import Any, Dict, Mapping

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.domains._domain import Domain

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class ForgeVerifyResponse(BaseResponse):
    """
    ForgeVerifyResponse is the slim acknowledgment returned when a Forge
    verification is triggered. Verification runs asynchronously; poll
    `Domains.get` for the domain's state.

    Attributes:
        object (str): The object type, always "domain"
        id (str): The domain ID
    """

    object: str
    id: str


class DomainForge:
    class EnableParams(TypedDict):
        id: str
        """
        The domain ID.
        """
        return_path: NotRequired[str]
        """
        The subdomain for the Return-Path address. When omitted, Resend picks
        a suggested label based on the domain's current return path.
        """

    class UpdateParams(TypedDict):
        id: str
        """
        The domain ID.
        """
        return_path: str
        """
        The new subdomain for the Return-Path address.
        """

    @classmethod
    def enable(cls, params: EnableParams) -> Domain:
        """
        Activate Forge on an existing domain. Idempotent on the API side:
        enabling an already-migrated domain returns its current state.

        Args:
            params (EnableParams): The Forge enable parameters

        Returns:
            Domain: The full domain object
        """
        path = f"/domains/{params['id']}/forge"
        resp = request.Request[Domain](
            path=path, params=cls._body(params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> Domain:
        """
        Move the return path of a Forge domain and re-verify. After the domain
        verifies, the API refuses this with a 422 `return_path_unavailable`.

        Args:
            params (UpdateParams): The Forge update parameters

        Returns:
            Domain: The full domain object
        """
        path = f"/domains/{params['id']}/forge"
        resp = request.Request[Domain](
            path=path, params=cls._body(params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def verify(cls, domain_id: str) -> ForgeVerifyResponse:
        """
        Trigger asynchronous Forge verification for a domain. Poll
        `Domains.get` for the domain's state.

        Args:
            domain_id (str): The domain ID

        Returns:
            ForgeVerifyResponse: The object and ID of the domain being verified
        """
        path = f"/domains/{domain_id}/forge/verify"
        resp = request.Request[ForgeVerifyResponse](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def enable_async(cls, params: EnableParams) -> Domain:
        """
        Activate Forge on an existing domain (async). Idempotent on the API
        side: enabling an already-migrated domain returns its current state.

        Args:
            params (EnableParams): The Forge enable parameters

        Returns:
            Domain: The full domain object
        """
        path = f"/domains/{params['id']}/forge"
        resp = await AsyncRequest[Domain](
            path=path, params=cls._body(params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> Domain:
        """
        Move the return path of a Forge domain and re-verify (async). After
        the domain verifies, the API refuses this with a 422
        `return_path_unavailable`.

        Args:
            params (UpdateParams): The Forge update parameters

        Returns:
            Domain: The full domain object
        """
        path = f"/domains/{params['id']}/forge"
        resp = await AsyncRequest[Domain](
            path=path, params=cls._body(params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def verify_async(cls, domain_id: str) -> ForgeVerifyResponse:
        """
        Trigger asynchronous Forge verification for a domain (async). Poll
        `Domains.get_async` for the domain's state.

        Args:
            domain_id (str): The domain ID

        Returns:
            ForgeVerifyResponse: The object and ID of the domain being verified
        """
        path = f"/domains/{domain_id}/forge/verify"
        resp = await AsyncRequest[ForgeVerifyResponse](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp

    @staticmethod
    def _body(params: Mapping[str, Any]) -> Dict[str, Any]:
        """The id addresses the path, not the request body."""
        return {k: v for k, v in params.items() if k != "id"}
