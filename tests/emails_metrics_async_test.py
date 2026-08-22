import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendEmailsMetricsAsync(AsyncResendBaseTest):
    async def test_metrics_async_with_no_params(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-02T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered", "opened"],
                "dimensions": [],
                "granularity": "daily",
                "totals": {"delivered": 100, "opened": 40},
            }
        )
        metrics: resend.Emails.MetricsResponse = await resend.Emails.metrics_async()
        assert metrics["object"] == "metrics"
        assert metrics["totals"]["delivered"] == 100
        assert "data" not in metrics
        self.mock.assert_called_with(url="https://api.resend.com/emails/metrics")

    async def test_metrics_async_with_broadcast_dimension(self) -> None:
        self.set_mock_json(
            {
                "object": "metrics",
                "start_date": "2026-07-01T00:00:00.000Z",
                "end_date": "2026-07-08T00:00:00.000Z",
                "metrics": ["delivered", "opened"],
                "dimensions": ["broadcast"],
                "granularity": "daily",
                "totals": {"delivered": 100, "opened": 40},
                "data": [
                    {
                        "broadcast_id": "b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f",
                        "broadcast_name": "July Newsletter",
                        "delivered": 100,
                        "opened": 40,
                    },
                ],
            }
        )
        params: resend.Emails.MetricsParams = {"dimensions": ["broadcast"]}
        metrics: resend.Emails.MetricsResponse = await resend.Emails.metrics_async(
            params=params
        )
        assert metrics["dimensions"] == ["broadcast"]
        assert metrics["data"][0]["broadcast_name"] == "July Newsletter"
        self.mock.assert_called_with(
            url="https://api.resend.com/emails/metrics?dimensions=broadcast"
        )

    async def test_metrics_async_raises_when_email_and_broadcast_dimensions_combined(
        self,
    ) -> None:
        params: resend.Emails.MetricsParams = {
            "dimensions": ["email", "broadcast"],
        }
        with pytest.raises(ValueError):
            await resend.Emails.metrics_async(params=params)
        self.mock.assert_not_called()

    async def test_metrics_async_raises_when_broadcast_dimension_combined_with_email_id(
        self,
    ) -> None:
        params: resend.Emails.MetricsParams = {
            "dimensions": ["broadcast"],
            "email_id": ["4dd369bc-aa82-4ff3-97de-514ae3000ee0"],
        }
        with pytest.raises(ValueError):
            await resend.Emails.metrics_async(params=params)
        self.mock.assert_not_called()

    async def test_metrics_async_raises_when_email_dimension_combined_with_broadcast_id(
        self,
    ) -> None:
        params: resend.Emails.MetricsParams = {
            "dimensions": ["email"],
            "broadcast_id": ["b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f"],
        }
        with pytest.raises(ValueError):
            await resend.Emails.metrics_async(params=params)
        self.mock.assert_not_called()

    async def test_metrics_async_raises_when_email_id_and_broadcast_id_combined(
        self,
    ) -> None:
        params: resend.Emails.MetricsParams = {
            "email_id": ["4dd369bc-aa82-4ff3-97de-514ae3000ee0"],
            "broadcast_id": ["b3a6e6e2-9f2b-4e2a-9b1b-1a2b3c4d5e6f"],
        }
        with pytest.raises(ValueError):
            await resend.Emails.metrics_async(params=params)
        self.mock.assert_not_called()

    async def test_metrics_async_raises_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Emails.metrics_async()
