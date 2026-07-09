import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestDomainClaimsAsync(AsyncResendBaseTest):
    async def test_domain_claims_create_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain_claim",
                "id": "dacf4072-4119-4d88-932f-6c6126d3a9d1",
                "name": "example.com",
                "status": "pending",
                "domain_id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "region": "us-east-1",
                "record": {
                    "type": "TXT",
                    "name": "example.com",
                    "value": "resend-domain-verification=3f8a1c2d4e5b6a7f8091a2b3c4d5e6f7",
                    "ttl": "Auto",
                },
                "blocked_reason": None,
                "failure_reason": None,
                "created_at": "2026-06-16T17:12:02.059593+00:00",
                "expires_at": "2026-06-23T17:12:02.059593+00:00",
            }
        )

        params: resend.Domains.Claims.CreateParams = {
            "name": "example.com",
            "region": "us-east-1",
        }
        claim = await resend.Domains.Claims.create_async(params)
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"
        assert claim["status"] == "pending"
        assert claim["record"]["type"] == "TXT"

    async def test_domain_claims_create_async_with_options(self) -> None:
        self.set_mock_json(
            {
                "object": "domain_claim",
                "id": "dacf4072-4119-4d88-932f-6c6126d3a9d1",
                "name": "example.com",
                "status": "pending",
            }
        )

        params: resend.Domains.Claims.CreateParams = {
            "name": "example.com",
            "region": "us-east-1",
            "custom_return_path": "send",
            "open_tracking": True,
            "click_tracking": False,
            "tracking_subdomain": "links",
        }
        claim = await resend.Domains.Claims.create_async(params)
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"

    async def test_should_create_domain_claim_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Domains.Claims.CreateParams = {"name": "example.com"}
        with pytest.raises(NoContentError):
            _ = await resend.Domains.Claims.create_async(params)

    async def test_domain_claims_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain_claim",
                "id": "dacf4072-4119-4d88-932f-6c6126d3a9d1",
                "name": "example.com",
                "status": "blocked",
                "domain_id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "region": "us-east-1",
                "blocked_reason": "grace_period",
                "failure_reason": None,
                "created_at": "2026-06-16T17:12:02.059593+00:00",
                "expires_at": "2026-06-23T17:12:02.059593+00:00",
            }
        )

        claim = await resend.Domains.Claims.get_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"
        assert claim["status"] == "blocked"
        assert claim["blocked_reason"] == "grace_period"

    async def test_should_get_domain_claim_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Domains.Claims.get_async(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
            )

    async def test_domain_claims_verify_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain_claim",
                "id": "dacf4072-4119-4d88-932f-6c6126d3a9d1",
                "name": "example.com",
                "status": "pending",
                "domain_id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "region": "us-east-1",
            }
        )

        claim = await resend.Domains.Claims.verify_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"
        assert claim["status"] == "pending"

    async def test_should_verify_domain_claim_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Domains.Claims.verify_async(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
            )
