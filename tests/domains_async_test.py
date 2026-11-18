from unittest.mock import AsyncMock

import pytest
from typing_extensions import assert_type

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendDomainsAsync(AsyncResendBaseTest):
    async def test_domains_create_async(self) -> None:
        self.set_mock_json(
            {
                "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
                "name": "example.com",
                "created_at": "2023-03-28 17:12:02.059593+00",
                "status": "not_started",
                "records": [
                    {
                        "record": "SPF",
                        "name": "bounces",
                        "type": "MX",
                        "ttl": "Auto",
                        "status": "not_started",
                        "value": "feedback-smtp.us-east-1.amazonses.com",
                        "priority": 10,
                    },
                    {
                        "record": "SPF",
                        "name": "bounces",
                        "value": '"v=spf1 include:amazonses.com ~all"',
                        "type": "TXT",
                        "ttl": "Auto",
                        "status": "not_started",
                    },
                    {
                        "record": "DKIM",
                        "name": "nhapbbryle57yxg3fbjytyodgbt2kyyg._domainkey",
                        "value": "nhapbbryle57yxg3fbjytyodgbt2kyyg.dkim.amazonses.com.",
                        "type": "CNAME",
                        "status": "not_started",
                        "ttl": "Auto",
                    },
                    {
                        "record": "DKIM",
                        "name": "xbakwbe5fcscrhzshpap6kbxesf6pfgn._domainkey",
                        "value": "xbakwbe5fcscrhzshpap6kbxesf6pfgn.dkim.amazonses.com.",
                        "type": "CNAME",
                        "status": "not_started",
                        "ttl": "Auto",
                    },
                    {
                        "record": "DKIM",
                        "name": "txrcreso3dqbvcve45tqyosxwaegvhgn._domainkey",
                        "value": "txrcreso3dqbvcve45tqyosxwaegvhgn.dkim.amazonses.com.",
                        "type": "CNAME",
                        "status": "not_started",
                        "ttl": "Auto",
                    },
                ],
                "region": "us-east-1",
            }
        )

        create_params: resend.Domains.CreateParams = {
            "name": "example.com",
            "region": "us-east-1",
            "custom_return_path": "send",
        }
        domain = await resend.Domains.create_async(params=create_params)
        assert domain["id"] == "4dd369bc-aa82-4ff3-97de-514ae3000ee0"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-03-28 17:12:02.059593+00"
        assert domain["region"] == "us-east-1"

    async def test_should_create_domains_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        create_params: resend.Domains.CreateParams = {
            "name": "example.com",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Domains.create_async(params=create_params)

    async def test_domains_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "name": "example.com",
                "status": "not_started",
                "created_at": "2023-04-26 20:21:26.347412+00",
                "region": "us-east-1",
            }
        )

        domain = await resend.Domains.get_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-04-26 20:21:26.347412+00"
        assert domain["region"] == "us-east-1"

    async def test_should_get_domains_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Domains.get_async(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206"
            )

    async def test_domains_list_async(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {
                        "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
                        "name": "example.com",
                        "status": "not_started",
                        "created_at": "2023-03-28 17:12:02.059593+00",
                        "region": "us-east-1",
                    }
                ]
            }
        )

        domains = await resend.Domains.list_async()
        for domain in domains["data"]:
            assert domain["id"] == "4dd369bc-aa82-4ff3-97de-514ae3000ee0"
            assert domain["name"] == "example.com"
            assert domain["status"] == "not_started"
            assert domain["created_at"] == "2023-03-28 17:12:02.059593+00"
            assert domain["region"] == "us-east-1"

    async def test_should_list_domains_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Domains.list_async()

    async def test_domains_create_async_with_tracking_subdomain(self) -> None:
        self.set_mock_json(
            {
                "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
                "name": "example.com",
                "created_at": "2023-03-28 17:12:02.059593+00",
                "status": "not_started",
                "open_tracking": True,
                "click_tracking": True,
                "tracking_subdomain": "links",
                "records": [
                    {
                        "record": "DKIM",
                        "name": "nhapbbryle57yxg3fbjytyodgbt2kyyg._domainkey",
                        "value": "nhapbbryle57yxg3fbjytyodgbt2kyyg.dkim.amazonses.com.",
                        "type": "CNAME",
                        "status": "not_started",
                        "ttl": "Auto",
                    },
                    {
                        "record": "Tracking",
                        "name": "links.example.com",
                        "value": "links1.resend-dns.com",
                        "type": "CNAME",
                        "ttl": "Auto",
                        "status": "not_started",
                    },
                    {
                        "record": "TrackingCAA",
                        "name": "",
                        "value": '0 issue "amazon.com"',
                        "type": "CAA",
                        "ttl": "Auto",
                        "status": "not_started",
                    },
                ],
                "region": "us-east-1",
            }
        )

        create_params: resend.Domains.CreateParams = {
            "name": "example.com",
            "region": "us-east-1",
            "tracking_subdomain": "links",
            "click_tracking": True,
            "open_tracking": True,
        }
        domain = await resend.Domains.create_async(params=create_params)
        assert domain["id"] == "4dd369bc-aa82-4ff3-97de-514ae3000ee0"
        assert domain["open_tracking"] is True
        assert domain["click_tracking"] is True
        assert domain["tracking_subdomain"] == "links"
        tracking_record = next(
            (r for r in (domain["records"] or []) if r["record"] == "Tracking"), None
        )
        assert tracking_record is not None
        assert tracking_record["name"] == "links.example.com"
        assert tracking_record["value"] == "links1.resend-dns.com"
        assert tracking_record["type"] == "CNAME"
        tracking_caa_record = next(
            (r for r in (domain["records"] or []) if r["record"] == "TrackingCAA"),
            None,
        )
        assert tracking_caa_record is not None
        assert tracking_caa_record["type"] == "CAA"
        assert tracking_caa_record["value"] == '0 issue "amazon.com"'

    async def test_domains_get_async_with_tracking_fields(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "name": "example.com",
                "status": "not_started",
                "created_at": "2023-04-26 20:21:26.347412+00",
                "region": "us-east-1",
                "open_tracking": True,
                "click_tracking": True,
                "tracking_subdomain": "links",
                "records": [
                    {
                        "record": "Tracking",
                        "name": "links.example.com",
                        "value": "links1.resend-dns.com",
                        "type": "CNAME",
                        "ttl": "Auto",
                        "status": "verified",
                    },
                    {
                        "record": "TrackingCAA",
                        "name": "",
                        "value": '0 issue "amazon.com"',
                        "type": "CAA",
                        "ttl": "Auto",
                        "status": "verified",
                    },
                ],
            }
        )

        domain = await resend.Domains.get_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["open_tracking"] is True
        assert domain["click_tracking"] is True
        assert domain["tracking_subdomain"] == "links"
        tracking_caa_record = next(
            (r for r in (domain["records"] or []) if r["record"] == "TrackingCAA"),
            None,
        )
        assert tracking_caa_record is not None
        assert tracking_caa_record["type"] == "CAA"

    async def test_domains_update_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            }
        )

        update_params: resend.Domains.UpdateParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "click_tracking": True,
            "open_tracking": True,
            "tls": "enforced",
        }
        domain = await resend.Domains.update_async(params=update_params)
        assert_type(domain, resend.Domains.UpdateDomainResponse)
        assert domain["object"] == "domain"
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"

    async def test_domains_update_async_with_tracking_subdomain(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            }
        )

        update_params: resend.Domains.UpdateParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "tracking_subdomain": "links",
        }
        domain = await resend.Domains.update_async(params=update_params)
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"

    async def test_should_update_domains_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        update_params: resend.Domains.UpdateParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "click_tracking": True,
        }
        with pytest.raises(NoContentError):
            _ = await resend.Domains.update_async(params=update_params)

    async def test_domains_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "deleted": True,
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            }
        )

        domain = await resend.Domains.remove_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert_type(domain, resend.Domains.RemoveDomainResponse)
        assert domain["object"] == "domain"
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["deleted"] is True

    async def test_should_remove_domains_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Domains.remove_async(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206"
            )

    async def test_domains_verify_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            }
        )

        domain = await resend.Domains.verify_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert_type(domain, resend.Domains.VerifyDomainResponse)
        assert domain["object"] == "domain"
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"

    async def test_should_verify_domains_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Domains.verify_async(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206"
            )

    async def test_domains_verify_async_with_forge_scope(self) -> None:
        self.set_mock_json(
            {"object": "domain", "id": "d91cd9bd-1176-453e-8fc1-35364d380206"}
        )

        params: resend.Domains.VerifyParams = {"scope": ["forge"]}
        domain = await resend.Domains.verify_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
            params=params,
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/domains/d91cd9bd-1176-453e-8fc1-35364d380206/verify"
        )

    async def test_domains_create_async_returns_capabilities(self) -> None:
        self.set_mock_json(
            {
                "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
                "name": "example.com",
                "created_at": "2026-03-28 17:12:02.059593+00",
                "status": "not_started",
                "capabilities": {"sending": "enabled", "receiving": "enabled"},
                "records": [],
                "region": "us-east-1",
            }
        )

        params: resend.Domains.CreateParams = {
            "name": "example.com",
            "capabilities": {"receiving": "enabled"},
        }
        domain = await resend.Domains.create_async(params)
        assert_type(domain["capabilities"], resend.DomainCapabilities)
        assert domain["capabilities"]["sending"] == "enabled"
        assert domain["capabilities"]["receiving"] == "enabled"

    async def test_domains_get_async_returns_capabilities(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "name": "example.com",
                "status": "not_started",
                "created_at": "2026-04-26 20:21:26.347412+00",
                "region": "us-east-1",
                "capabilities": {"sending": "enabled", "receiving": "disabled"},
                "records": [],
            }
        )

        domain = await resend.Domains.get_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206"
        )
        assert_type(domain["capabilities"], resend.DomainCapabilities)
        assert domain["capabilities"]["sending"] == "enabled"
        assert domain["capabilities"]["receiving"] == "disabled"

    async def test_domains_list_async_returns_capabilities(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                        "name": "example.com",
                        "status": "not_started",
                        "created_at": "2026-04-26 20:21:26.347412+00",
                        "region": "us-east-1",
                        "capabilities": {
                            "sending": "enabled",
                            "receiving": "disabled",
                        },
                    }
                ],
            }
        )

        domains = await resend.Domains.list_async()
        assert_type(domains["data"][0]["capabilities"], resend.DomainCapabilities)
        assert domains["data"][0]["capabilities"]["sending"] == "enabled"
        assert domains["data"][0]["capabilities"]["receiving"] == "disabled"


class TestDomainsRequestBodyAsync:
    def setup_method(self) -> None:
        self.previous_api_key = resend.api_key
        resend.api_key = "re_123"
        self.mock_client = AsyncMock()
        self.mock_client.request.return_value = (
            b'{"object": "domain", "id": "479e3145-dd38-476b-932c-529ceb705947"}',
            200,
            {"content-type": "application/json"},
        )
        self.previous_async_http_client = resend.default_async_http_client
        resend.default_async_http_client = self.mock_client

    def teardown_method(self) -> None:
        resend.default_async_http_client = self.previous_async_http_client
        resend.api_key = self.previous_api_key

    async def test_create_async_sends_tls_and_capabilities(self) -> None:
        params: resend.Domains.CreateParams = {
            "name": "example.com",
            "tls": "enforced",
            "capabilities": {"sending": "enabled", "receiving": "enabled"},
        }
        self.mock_client.request.return_value = (
            b'{"id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0", "name": "example.com",'
            b' "created_at": "2026-03-28 17:12:02.059593+00", "status": "not_started",'
            b' "region": "us-east-1", "records": [],'
            b' "capabilities": {"sending": "enabled", "receiving": "enabled"}}',
            200,
            {"content-type": "application/json"},
        )
        domain = await resend.Domains.create_async(params)
        assert domain["capabilities"]["receiving"] == "enabled"

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["method"] == "post"
        assert kwargs["url"] == f"{resend.api_url}/domains"
        assert kwargs["json"] == {
            "name": "example.com",
            "tls": "enforced",
            "capabilities": {"sending": "enabled", "receiving": "enabled"},
        }

    async def test_update_async_sends_a_single_capability(self) -> None:
        params: resend.Domains.UpdateParams = {
            "id": "479e3145-dd38-476b-932c-529ceb705947",
            "capabilities": {"receiving": "enabled"},
        }
        await resend.Domains.update_async(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["method"] == "patch"
        assert (
            kwargs["url"]
            == f"{resend.api_url}/domains/479e3145-dd38-476b-932c-529ceb705947"
        )
        assert kwargs["json"]["capabilities"] == {"receiving": "enabled"}
