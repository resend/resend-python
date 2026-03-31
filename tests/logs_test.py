import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendLogs(ResendBaseTest):
    def test_logs_get(self) -> None:
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

        log: resend.Logs.GetResponse = resend.Logs.get(
            "37e4414c-5e25-4dbc-a071-43552a4bd53b"
        )
        assert log["object"] == "log"
        assert log["id"] == "37e4414c-5e25-4dbc-a071-43552a4bd53b"
        assert log["created_at"] == "2024-01-01T00:00:00.000000+00:00"
        assert log["endpoint"] == "/emails"
        assert log["method"] == "POST"
        assert log["response_status"] == 200
        assert log["user_agent"] == "resend-python/2.0.0"
        assert log["request_body"] == {"to": ["user@example.com"], "subject": "Hello"}
        assert log["response_body"] == {"id": "email-id-123"}

    def test_should_get_log_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Logs.get("37e4414c-5e25-4dbc-a071-43552a4bd53b")

    def test_logs_list(self) -> None:
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

        logs: resend.Logs.ListResponse = resend.Logs.list()
        assert logs["object"] == "list"
        assert logs["has_more"] is False
        assert len(logs["data"]) == 1
        log = logs["data"][0]
        assert log["id"] == "37e4414c-5e25-4dbc-a071-43552a4bd53b"
        assert log["created_at"] == "2024-01-01T00:00:00.000000+00:00"
        assert log["endpoint"] == "/emails"
        assert log["method"] == "POST"
        assert log["response_status"] == 200
        assert log["user_agent"] == "resend-python/2.0.0"

    def test_should_list_logs_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Logs.list()

    def test_logs_list_with_pagination_params(self) -> None:
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
                    },
                    {
                        "id": "log-id-2",
                        "created_at": "2024-01-02T00:00:00.000000+00:00",
                        "endpoint": "/domains",
                        "method": "GET",
                        "response_status": 200,
                        "user_agent": "resend-python/2.0.0",
                    },
                ],
            }
        )

        params: resend.Logs.ListParams = {"limit": 10, "after": "previous-log-id"}
        logs: resend.Logs.ListResponse = resend.Logs.list(params=params)
        assert logs["object"] == "list"
        assert logs["has_more"] is True
        assert len(logs["data"]) == 2
        assert logs["data"][0]["id"] == "log-id-1"
        assert logs["data"][1]["id"] == "log-id-2"

    def test_logs_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "log-id-3",
                        "created_at": "2024-01-03T00:00:00.000000+00:00",
                        "endpoint": "/api-keys",
                        "method": "DELETE",
                        "response_status": 200,
                        "user_agent": "resend-python/2.0.0",
                    }
                ],
            }
        )

        params: resend.Logs.ListParams = {"limit": 5, "before": "later-log-id"}
        logs: resend.Logs.ListResponse = resend.Logs.list(params=params)
        assert logs["object"] == "list"
        assert logs["has_more"] is False
        assert len(logs["data"]) == 1
        assert logs["data"][0]["id"] == "log-id-3"
