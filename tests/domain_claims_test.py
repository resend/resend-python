import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestDomainClaims(ResendBaseTest):
    def test_domain_claims_create(self) -> None:
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
        claim: resend.DomainClaim = resend.Domains.Claims.create(params)
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"
        assert claim["object"] == "domain_claim"
        assert claim["name"] == "example.com"
        assert claim["status"] == "pending"
        assert claim["domain_id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert claim["record"]["type"] == "TXT"
        assert (
            claim["record"]["value"]
            == "resend-domain-verification=3f8a1c2d4e5b6a7f8091a2b3c4d5e6f7"
        )
        assert claim["blocked_reason"] is None
        assert claim["failure_reason"] is None

    def test_domain_claims_create_with_options(self) -> None:
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
        claim = resend.Domains.Claims.create(params)
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"

    def test_should_create_domain_claim_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Domains.Claims.CreateParams = {"name": "example.com"}
        with self.assertRaises(NoContentError):
            _ = resend.Domains.Claims.create(params)

    def test_domain_claims_get(self) -> None:
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

        claim = resend.Domains.Claims.get(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"
        assert claim["status"] == "blocked"
        assert claim["blocked_reason"] == "grace_period"

    def test_should_get_domain_claim_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Domains.Claims.get(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
            )

    def test_domain_claims_verify(self) -> None:
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

        claim = resend.Domains.Claims.verify(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert claim["id"] == "dacf4072-4119-4d88-932f-6c6126d3a9d1"
        assert claim["status"] == "pending"

    def test_should_verify_domain_claim_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Domains.Claims.verify(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
            )
