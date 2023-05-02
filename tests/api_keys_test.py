import unittest
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class TestResendApiKeys(unittest.TestCase):
    def test_api_keys_create(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json():
            return {
                "id": "dacf4072-4119-4d88-932f-6202748ac7c8",
                "token": "re_c1tpEyD8_NKFusih9vKVQknRAQfmFcWCv",
            }

        m.json = mock_json
        mock.return_value = m

        params = {
            "name": "prod",
        }
        key = resend.ApiKeys.create(params)
        assert key["id"] == "dacf4072-4119-4d88-932f-6202748ac7c8"
        patcher.stop()

    def test_api_keys_list(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json():
            return {
                "data": [
                    {
                        "id": "91f3200a-df72-4654-b0cd-f202395f5354",
                        "name": "Production",
                        "created_at": "2023-04-08T00:11:13.110779+00:00",
                    }
                ]
            }

        m.json = mock_json
        mock.return_value = m

        keys = resend.ApiKeys.list()
        assert keys["data"][0]["id"] == "91f3200a-df72-4654-b0cd-f202395f5354"
        patcher.stop()

    def test_api_keys_remove(self):
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        m.text = ""
        mock.return_value = m

        email = resend.ApiKeys.remove(
            api_key_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        )
        assert email is None
        patcher.stop()
