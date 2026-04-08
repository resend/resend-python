import pytest

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
                "created_at": "2023-03-28T17:12:02.059593+00:00",
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
        assert domain["created_at"] == "2023-03-28T17:12:02.059593+00:00"
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
                "created_at": "2023-04-26T20:21:26.347412+00:00",
                "region": "us-east-1",
            }
        )

        domain = await resend.Domains.get_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-04-26T20:21:26.347412+00:00"
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
                        "created_at": "2023-03-28T17:12:02.059593+00:00",
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
            assert domain["created_at"] == "2023-03-28T17:12:02.059593+00:00"
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
                "created_at": "2023-03-28T17:12:02.059593+00:00",
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
                ],
                "region": "us-east-1",
            }
        )

        create_params: resend.Domains.CreateParams = {
            "name": "example.com",
            "region": "us-east-1",
            "tracking_subdomain": "links",
        }
        domain = await resend.Domains.create_async(params=create_params)
        assert domain["id"] == "4dd369bc-aa82-4ff3-97de-514ae3000ee0"
        assert domain["open_tracking"] is True
        assert domain["click_tracking"] is True
        assert domain["tracking_subdomain"] == "links"
        tracking_record = next(
            (r for r in domain["records"] if r["record"] == "Tracking"), None
        )
        assert tracking_record is not None
        assert tracking_record["name"] == "links.example.com"
        assert tracking_record["value"] == "links1.resend-dns.com"
        assert tracking_record["type"] == "CNAME"

    async def test_domains_get_async_with_tracking_fields(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "name": "example.com",
                "status": "not_started",
                "created_at": "2023-04-26T20:21:26.347412+00:00",
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
                    }
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

    async def test_domains_update_async(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "name": "example.com",
                "status": "not_started",
                "created_at": "2023-04-26T20:21:26.347412+00:00",
                "region": "us-east-1",
            }
        )

        update_params: resend.Domains.UpdateParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "click_tracking": True,
            "open_tracking": True,
            "tls": "enforced",
        }
        domain = await resend.Domains.update_async(params=update_params)
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-04-26T20:21:26.347412+00:00"
        assert domain["region"] == "us-east-1"

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
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "name": "example.com",
                "status": "not_started",
                "created_at": "2023-04-26T20:21:26.347412+00:00",
                "region": "us-east-1",
            }
        )

        domain = await resend.Domains.remove_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-04-26T20:21:26.347412+00:00"
        assert domain["region"] == "us-east-1"

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
                "name": "example.com",
                "status": "verified",
                "created_at": "2023-04-26T20:21:26.347412+00:00",
                "region": "us-east-1",
            }
        )

        domain = await resend.Domains.verify_async(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "verified"
        assert domain["created_at"] == "2023-04-26T20:21:26.347412+00:00"
        assert domain["region"] == "us-east-1"

    async def test_should_verify_domains_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Domains.verify_async(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206"
            )
