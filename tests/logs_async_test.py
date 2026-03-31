import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendLogsAsync(AsyncResendBaseTest):
    async def test_logs_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "log",
                "id": "37e4414c-5e25-4dbc-a071-43552a4bd53b",
                "created_at": "2024-01-01T00:00:00.000000+00:00",
                "endpoint": "/emails",
                "method": "POST",
                "response_status": 200,
                "user_agent": "resend-python/2.0.0",
                "request_body": {"to": ["user@example.com"], "subject": "Hello"},
                "response_body": {"id": "email-id-123"},
            }
        )

        log: resend.Logs.GetResponse = await resend.Logs.get_async(
            "37e4414c-5e25-4dbc-a071-43552a4bd53b"
        )
        assert log["object"] == "log"
        assert log["id"] == "37e4414c-5e25-4dbc-a071-43552a4bd53b"
        assert log["endpoint"] == "/emails"
        assert log["method"] == "POST"
        assert log["response_status"] == 200

    async def test_should_get_log_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Logs.get_async("37e4414c-5e25-4dbc-a071-43552a4bd53b")

    async def test_logs_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "37e4414c-5e25-4dbc-a071-43552a4bd53b",
                        "created_at": "2024-01-01T00:00:00.000000+00:00",
                        "endpoint": "/emails",
                        "method": "POST",
                        "response_status": 200,
                        "user_agent": "resend-python/2.0.0",
                    }
                ],
            }
        )

        logs: resend.Logs.ListResponse = await resend.Logs.list_async()
        assert logs["object"] == "list"
        assert logs["has_more"] is False
        for log in logs["data"]:
            assert log["id"] == "37e4414c-5e25-4dbc-a071-43552a4bd53b"
            assert log["endpoint"] == "/emails"

    async def test_should_list_logs_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Logs.list_async()

    async def test_logs_list_async_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "log-id-1",
                        "created_at": "2024-01-01T00:00:00.000000+00:00",
                        "endpoint": "/emails",
                        "method": "POST",
                        "response_status": 200,
                        "user_agent": "resend-python/2.0.0",
                    }
                ],
            }
        )

        params: resend.Logs.ListParams = {"limit": 10, "after": "previous-log-id"}
        logs: resend.Logs.ListResponse = await resend.Logs.list_async(params=params)
        assert logs["has_more"] is True
        assert logs["data"][0]["id"] == "log-id-1"
