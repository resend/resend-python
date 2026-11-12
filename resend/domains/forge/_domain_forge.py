from typing import Any, Dict, Mapping

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.domains._domain import Domain

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class DomainForge:
    class EnableParams(TypedDict):
        id: str
        """
        The domain ID.
        """
        return_path: NotRequired[str]
        """
        The subdomain for the Return-Path address. When omitted, Resend picks
        a free DNS label for the domain.
        """

    @classmethod
    def enable(cls, params: EnableParams) -> Domain:
        """
        Activate Forge on an existing domain. Idempotent on the API side:
        enabling an already-migrated domain returns its current state.

        To move the Forge return path afterwards, use `Domains.update` with
        `forge_return_path`. To re-check only the Forge record, use
        `Domains.verify` with `scope=["forge"]`.

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
    async def enable_async(cls, params: EnableParams) -> Domain:
        """
        Activate Forge on an existing domain (async). Idempotent on the API
        side: enabling an already-migrated domain returns its current state.

        To move the Forge return path afterwards, use `Domains.update_async`
        with `forge_return_path`. To re-check only the Forge record, use
        `Domains.verify_async` with `scope=["forge"]`.

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

    @staticmethod
    def _body(params: Mapping[str, Any]) -> Dict[str, Any]:
        """The id addresses the path, not the request body."""
        return {k: v for k, v in params.items() if k != "id"}
