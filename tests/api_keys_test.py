import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendApiKeys(ResendBaseTest):
    def test_api_keys_create(self) -> None:
        self.set_mock_json(
            {
                "id": "dacf4072-4119-4d88-932f-6202748ac7c8",
                "token": "re_c1tpEyD8_NKFusih9vKVQknRAQfmFcWCv",
            }
        )

        params: resend.ApiKeys.CreateParams = {
            "name": "prod",
        }
        key: resend.ApiKeys.CreateApiKeyResponse = resend.ApiKeys.create(params)
        assert key["id"] == "dacf4072-4119-4d88-932f-6202748ac7c8"

    def test_should_create_api_key_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.ApiKeys.CreateParams = {
            "name": "prod",
        }
        with self.assertRaises(NoContentError):
            _ = resend.ApiKeys.create(params)

    def test_api_keys_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "91f3200a-df72-4654-b0cd-f202395f5354",
                        "name": "Production",
                        "created_at": "2023-04-08T00:11:13.110779+00:00",
                    }
                ],
            }
        )

        keys: resend.ApiKeys.ListResponse = resend.ApiKeys.list()
        assert keys["object"] == "list"
        assert keys["has_more"] is False
        for key in keys["data"]:
            assert key["id"] == "91f3200a-df72-4654-b0cd-f202395f5354"
            assert key["name"] == "Production"
            assert key["created_at"] == "2023-04-08T00:11:13.110779+00:00"

    def test_should_list_api_key_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.ApiKeys.list()

    def test_api_keys_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "test-key-1",
                        "name": "Test Key 1",
                        "created_at": "2023-04-08T00:11:13.110779+00:00",
                    },
                    {
                        "id": "test-key-2",
                        "name": "Test Key 2",
                        "created_at": "2023-04-09T00:11:13.110779+00:00",
                    },
                ],
            }
        )

        params: resend.ApiKeys.ListParams = {"limit": 10, "after": "previous-key-id"}
        keys: resend.ApiKeys.ListResponse = resend.ApiKeys.list(params=params)
        assert keys["object"] == "list"
        assert keys["has_more"] is True
        assert len(keys["data"]) == 2
        assert keys["data"][0]["id"] == "test-key-1"
        assert keys["data"][1]["id"] == "test-key-2"

    def test_api_keys_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "test-key-3",
                        "name": "Test Key 3",
                        "created_at": "2023-04-07T00:11:13.110779+00:00",
                    }
                ],
            }
        )

        params: resend.ApiKeys.ListParams = {"limit": 5, "before": "later-key-id"}
        keys: resend.ApiKeys.ListResponse = resend.ApiKeys.list(params=params)
        assert keys["object"] == "list"
        assert keys["has_more"] is False
        assert len(keys["data"]) == 1
        assert keys["data"][0]["id"] == "test-key-3"

    def test_api_keys_remove(self) -> None:
        self.set_mock_text("")

        assert (
            resend.ApiKeys.remove(
                api_key_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
            )
            is None
        )
