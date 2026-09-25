import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendUsage(ResendBaseTest):
    def test_usage_get(self) -> None:
        self.set_mock_json(
            {
                "object": "usage",
                "emails": {
                    "daily": {
                        "used": 258,
                        "limit": None,
                        "sent": 57,
                        "received": 201,
                        "resets_at": "2026-07-17T00:00:00.000Z",
                    },
                    "monthly": {
                        "used": 5442,
                        "limit": 10000,
                        "sent": 1000,
                        "received": 4442,
                        "resets_at": "2026-08-01T00:00:00.000Z",
                    },
                },
                "contacts": {"used": 85000, "limit": 150000},
                "segments": {"used": 2, "limit": 3},
                "broadcasts": {"used": 100, "limit": None},
                "ai_credits": {
                    "used": 0,
                    "limit": 500,
                    "next_increase_at": "2026-07-18T09:00:00.000Z",
                },
                "automation_runs": {
                    "used": 0,
                    "limit": 1000,
                    "resets_at": "2026-08-01T00:00:00.000Z",
                },
                "domains": {"used": 1, "limit": 1000},
                "rate_limit": {"limit": 10, "duration": "1000ms"},
            }
        )

        usage: resend.Usage.GetResponse = resend.Usage.get()
        assert usage["object"] == "usage"
        assert usage["emails"]["daily"]["used"] == 258
        assert usage["emails"]["daily"]["limit"] is None
        assert usage["emails"]["daily"]["sent"] == 57
        assert usage["emails"]["daily"]["received"] == 201
        assert usage["emails"]["daily"]["resets_at"] == "2026-07-17T00:00:00.000Z"
        assert usage["emails"]["monthly"]["used"] == 5442
        assert usage["emails"]["monthly"]["limit"] == 10000
        assert usage["contacts"]["used"] == 85000
        assert usage["contacts"]["limit"] == 150000
        assert usage["segments"]["used"] == 2
        assert usage["segments"]["limit"] == 3
        assert usage["broadcasts"]["used"] == 100
        assert usage["broadcasts"]["limit"] is None
        assert usage["ai_credits"]["used"] == 0
        assert usage["ai_credits"]["limit"] == 500
        assert usage["ai_credits"]["next_increase_at"] == "2026-07-18T09:00:00.000Z"
        assert usage["automation_runs"]["used"] == 0
        assert usage["automation_runs"]["limit"] == 1000
        assert usage["automation_runs"]["resets_at"] == "2026-08-01T00:00:00.000Z"
        assert usage["domains"]["used"] == 1
        assert usage["domains"]["limit"] == 1000
        assert usage["rate_limit"]["limit"] == 10
        assert usage["rate_limit"]["duration"] == "1000ms"

    def test_should_get_usage_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Usage.get()
