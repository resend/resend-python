from typing import Any, Dict, cast

from typing_extensions import NotRequired, TypedDict

from resend import request

from ._domain_claim import DomainClaim

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class DomainClaims:
    class CreateParams(TypedDict):
        name: str
        """
        The name of the domain you want to claim.
        """
        region: NotRequired[str]
        """
        The region where emails will be sent from.
        Possible values: 'us-east-1' | 'eu-west-1' | 'sa-east-1' | 'ap-northeast-1'
        """
        custom_return_path: NotRequired[str]
        """
        By default, Resend will use the `send` subdomain for the Return-Path address.
        You can change this by setting the optional `custom_return_path` parameter.
        """
        tracking_subdomain: NotRequired[str]
        """
        The custom subdomain used for click and open tracking links (e.g., "links").
        """
        click_tracking: NotRequired[bool]
        """
        Track clicks within the body of each HTML email.
        """
        open_tracking: NotRequired[bool]
        """
        Track the open rate of each email.
        """

    @classmethod
    def create(cls, params: CreateParams) -> DomainClaim:
        """
        Start a claim for a domain that another Resend account has already verified.
        The domain is recreated under your account with fresh DKIM keys, so the
        previous account's DNS records cannot be reused.
        see more: https://resend.com/docs/api-reference/domains/claim-domain

        Args:
            params (CreateParams): The domain claim parameters

        Returns:
            DomainClaim: The created domain claim, or an identical pending claim
                if one already existed
        """
        path = "/domains/claim"
        resp = request.Request[DomainClaim](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, domain_id: str) -> DomainClaim:
        """
        Retrieve the latest claim for the placeholder domain created by the claim.
        see more: https://resend.com/docs/api-reference/domains/get-domain-claim

        Args:
            domain_id (str): The ID of the placeholder domain created by the claim

        Returns:
            DomainClaim: The domain claim object
        """
        path = f"/domains/{domain_id}/claim"
        resp = request.Request[DomainClaim](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def verify(cls, domain_id: str) -> DomainClaim:
        """
        Trigger asynchronous DNS verification and ownership transfer for a domain
        claim. The claim stays 'pending' while verification runs; poll `get` for
        status.
        see more: https://resend.com/docs/api-reference/domains/verify-domain-claim

        Args:
            domain_id (str): The ID of the placeholder domain created by the claim

        Returns:
            DomainClaim: The domain claim object
        """
        path = f"/domains/{domain_id}/claim/verify"
        resp = request.Request[DomainClaim](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(cls, params: CreateParams) -> DomainClaim:
        """
        Start a claim for a domain that another Resend account has already verified
        (async). The domain is recreated under your account with fresh DKIM keys, so
        the previous account's DNS records cannot be reused.
        see more: https://resend.com/docs/api-reference/domains/claim-domain

        Args:
            params (CreateParams): The domain claim parameters

        Returns:
            DomainClaim: The created domain claim, or an identical pending claim
                if one already existed
        """
        path = "/domains/claim"
        resp = await AsyncRequest[DomainClaim](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, domain_id: str) -> DomainClaim:
        """
        Retrieve the latest claim for the placeholder domain created by the claim
        (async).
        see more: https://resend.com/docs/api-reference/domains/get-domain-claim

        Args:
            domain_id (str): The ID of the placeholder domain created by the claim

        Returns:
            DomainClaim: The domain claim object
        """
        path = f"/domains/{domain_id}/claim"
        resp = await AsyncRequest[DomainClaim](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def verify_async(cls, domain_id: str) -> DomainClaim:
        """
        Trigger asynchronous DNS verification and ownership transfer for a domain
        claim (async). The claim stays 'pending' while verification runs; poll
        `get_async` for status.
        see more: https://resend.com/docs/api-reference/domains/verify-domain-claim

        Args:
            domain_id (str): The ID of the placeholder domain created by the claim

        Returns:
            DomainClaim: The domain claim object
        """
        path = f"/domains/{domain_id}/claim/verify"
        resp = await AsyncRequest[DomainClaim](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp
