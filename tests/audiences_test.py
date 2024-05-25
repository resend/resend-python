import unittest
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class TestResendAudiences(unittest.TestCase):
    def test_audiences_create(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
            }

        m.json = mock_json
        mock.return_value = m

        params: resend.Audiences.CreateParams = {
            "name": "Python SDK Audience",
        }
        audience = resend.Audiences.create(params)
        assert audience["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audience["name"] == "Registered Users"

        patcher.stop()

    def test_audiences_get(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
                "created_at": "2023-10-06T22:59:55.977Z",
            }

        m.json = mock_json
        mock.return_value = m

        audience = resend.Audiences.get(id="78261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert audience["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audience["name"] == "Registered Users"
        assert audience["created_at"] == "2023-10-06T22:59:55.977Z"
        patcher.stop()

    def test_audiences_remove(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }

        m.json = mock_json
        mock.return_value = m

        rmed = resend.Audiences.remove("78261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

        patcher.stop()

    def test_audiences_list(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "list",
                "data": [
                    {
                        "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "name": "Registered Users",
                        "created_at": "2023-10-06T22:59:55.977Z",
                    }
                ],
            }

        m.json = mock_json
        mock.return_value = m

        audiences: resend.Audiences.ListResponse = resend.Audiences.list()
        assert audiences["data"][0]["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert audiences["data"][0]["name"] == "Registered Users"
        patcher.stop()
