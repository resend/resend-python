from typing import Any, Dict
from unittest import TestCase
from unittest.mock import create_autospec

import resend
from resend.exceptions import NoContentError
from resend.http_client import HTTPClient
from tests.conftest import ResendBaseTest

# flake8: noqa


def forge_domain_json() -> Dict[str, Any]:
    return {
        "object": "domain",
        "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
        "name": "example.com",
        "status": "pending",
        "created_at": "2026-11-11 10:00:00.000000+00",
        "region": "us-east-1",
        "records": [
            {
                "record": "SPF",
                "name": "send",
                "value": "v=spf1 include:spf.resend.com ~all",
                "type": "TXT",
                "ttl": "Auto",
                "status": "pending",
            },
            {
                "record": "DKIM",
                "name": "resend._domainkey",
                "value": "resend._domainkey.example.com.dkim.resend.com.",
                "type": "CNAME",
                "ttl": "Auto",
                "status": "pending",
            },
        ],
        "open_tracking": False,
        "click_tracking": False,
    }


class TestDomainForge(ResendBaseTest):
    def test_domain_forge_enable(self) -> None:
        self.set_mock_json(forge_domain_json())

        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "return_path": "send",
        }
        domain: resend.Domain = resend.Domains.Forge.enable(params)
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "pending"
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/domains/d91cd9bd-1176-453e-8fc1-35364d380206/forge"
        )

    def test_domain_forge_enable_without_return_path(self) -> None:
        self.set_mock_json(forge_domain_json())

        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
        }
        domain = resend.Domains.Forge.enable(params)
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["status"] == "pending"

    def test_should_enable_forge_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Domains.Forge.enable(params)

    def test_domain_forge_update(self) -> None:
        self.set_mock_json(forge_domain_json())

        params: resend.Domains.Forge.UpdateParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "return_path": "outbound",
        }
        domain: resend.Domain = resend.Domains.Forge.update(params)
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/domains/d91cd9bd-1176-453e-8fc1-35364d380206/forge"
        )

    def test_should_update_forge_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Domains.Forge.UpdateParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "return_path": "outbound",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Domains.Forge.update(params)

    def test_domain_forge_verify(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            }
        )

        verified: resend.ForgeVerifyResponse = resend.Domains.Forge.verify(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206"
        )
        assert verified["object"] == "domain"
        assert verified["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/domains/d91cd9bd-1176-453e-8fc1-35364d380206/forge/verify"
        )

    def test_should_verify_forge_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Domains.Forge.verify(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206"
            )


class TestDomainForgeRequestBody(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_123"
        self.mock_client = create_autospec(HTTPClient, instance=True)
        self.mock_client.request.return_value = (
            b'{"id": "d91cd9bd-1176-453e-8fc1-35364d380206"}',
            200,
            {"Content-Type": "application/json"},
        )
        self.previous_http_client = resend.default_http_client
        resend.default_http_client = self.mock_client

    def tearDown(self) -> None:
        resend.default_http_client = self.previous_http_client

    def test_enable_sends_snake_case_return_path_and_no_id(self) -> None:
        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "return_path": "send",
        }
        resend.Domains.Forge.enable(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["method"] == "post"
        assert kwargs["json"] == {"return_path": "send"}

    def test_enable_sends_empty_body_without_return_path(self) -> None:
        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
        }
        resend.Domains.Forge.enable(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["method"] == "post"
        assert kwargs["json"] == {}

    def test_update_sends_return_path_with_patch(self) -> None:
        params: resend.Domains.Forge.UpdateParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "return_path": "outbound",
        }
        resend.Domains.Forge.update(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["method"] == "patch"
        assert kwargs["json"] == {"return_path": "outbound"}
