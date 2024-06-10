import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendDomains(ResendBaseTest):
    def test_domains_create(self) -> None:
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
        }
        domain = resend.Domains.create(params=create_params)
        assert domain["id"] == "4dd369bc-aa82-4ff3-97de-514ae3000ee0"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-03-28T17:12:02.059593+00:00"
        assert domain["region"] == "us-east-1"

    def test_should_create_domains_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        create_params: resend.Domains.CreateParams = {
            "name": "example.com",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Domains.create(params=create_params)

    def test_domains_get(self) -> None:
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

        domain = resend.Domains.get(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"
        assert domain["status"] == "not_started"
        assert domain["created_at"] == "2023-04-26T20:21:26.347412+00:00"
        assert domain["region"] == "us-east-1"

    def test_should_get_domains_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Domains.get(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
            )

    def test_domains_list(self) -> None:
        self.set_mock_json(
            {
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
        )

        domains = resend.Domains.list()
        assert domains["data"][0]["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domains["data"][0]["name"] == "example.com"
        assert domains["data"][0]["status"] == "not_started"
        assert domains["data"][0]["created_at"] == "2023-04-26T20:21:26.347412+00:00"
        assert domains["data"][0]["region"] == "us-east-1"

    def test_should_list_domains_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Domains.list()

    def test_domains_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                "deleted": True,
            }
        )

        domain = resend.Domains.remove(
            domain_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        )
        assert domain["deleted"] is True
        assert domain["id"] == "4ef9a417-02e9-4d39-ad75-9611e0fcc33c"

    def test_should_remove_domains_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Domains.remove(
                domain_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
            )

    def test_domains_verify(self) -> None:
        self.set_mock_json(
            {"object": "domain", "id": "d91cd9bd-1176-453e-8fc1-35364d380206"}
        )

        domain = resend.Domains.verify(
            domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
        )
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"

    def test_should_verify_domains_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Domains.verify(
                domain_id="d91cd9bd-1176-453e-8fc1-35364d380206",
            )

    def test_domains_update(self) -> None:
        self.set_mock_json(
            {
                "object": "domain",
                "id": "479e3145-dd38-476b-932c-529ceb705947",
            }
        )

        params: resend.Domains.UpdateParams = {
            "id": "479e3145-dd38-476b-932c-529ceb705947",
            "open_tracking": True,
            "click_tracking": True,
            "tls": "opportunistic",
        }
        domain = resend.Domains.update(params)
        assert domain["id"] == "479e3145-dd38-476b-932c-529ceb705947"

    def test_should_update_domains_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Domains.UpdateParams = {
            "id": "479e3145-dd38-476b-932c-529ceb705947",
            "open_tracking": True,
            "click_tracking": True,
        }
        with self.assertRaises(NoContentError):
            _ = resend.Domains.update(params)
