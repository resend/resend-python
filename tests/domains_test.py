import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class TestResendDomains(unittest.TestCase):
    def test_domains_create(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
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

        m.json = mock_json
        mock.return_value = m

        create_params: resend.Domains.CreateParams = {
            "name": "example.com",
        }
        domain = resend.Domains.create(params=create_params)
        assert domain["id"] == "4dd369bc-aa82-4ff3-97de-514ae3000ee0"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-03-28T17:12:02.059593+00:00"
        assert domain["region"] == "us-east-1"

        patcher.stop()

    def test_domains_get(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "domain",
                "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                "name": "example.com",
                "status": "not_started",
                "created_at": "2023-04-26T20:21:26.347412+00:00",
                "region": "us-east-1",
            }

        m.json = mock_json
        mock.return_value = m

        domain = resend.Domains.get(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-04-26T20:21:26.347412+00:00"
        assert domain["region"] == "us-east-1"
        patcher.stop()

    def test_domains_list(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "data": [
                    {
                        "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
                        "name": "example.com",
                        "status": "not_started",
                        "created_at": "2023-04-26T20:21:26.347412+00:00",
                        "region": "us-east-1",
                    }
                ]
            }

        m.json = mock_json
        mock.return_value = m

        domains = resend.Domains.list()
        assert domains["data"][0]["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domains["data"][0]["name"] == "example.com"
        assert domains["data"][0]["status"] == "not_started"
        assert domains["data"][0]["created_at"] == "2023-04-26T20:21:26.347412+00:00"
        assert domains["data"][0]["region"] == "us-east-1"
        patcher.stop()

    def test_domains_remove(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "domain",
                "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                "deleted": True,
            }

        m.json = mock_json
        mock.return_value = m

        domain = resend.Domains.remove(
            domain_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        )
        assert domain["deleted"] is True
        assert domain["id"] == "4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
        patcher.stop()

    def test_domains_verify(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {"object": "domain", "id": "d91cd9bd-1176-453e-8fc1-35364d380206"}

        m.json = mock_json
        mock.return_value = m

        domain = resend.Domains.verify(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"

        patcher.stop()

    def test_domains_update(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "domain",
                "id": "479e3145-dd38-476b-932c-529ceb705947",
            }

        m.json = mock_json
        mock.return_value = m

        params: resend.Domains.UpdateParams = {
            "id": "479e3145-dd38-476b-932c-529ceb705947",
            "open_tracking": True,
            "click_tracking": True,
        }
        domain = resend.Domains.update(params)
        assert domain["id"] == "479e3145-dd38-476b-932c-529ceb705947"

        patcher.stop()
