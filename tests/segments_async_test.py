import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendSegmentsAsync(AsyncResendBaseTest):
    async def test_segments_update_async(self) -> None:
        self.set_mock_json(
            {
                "object": "segment",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        params: resend.Segments.UpdateParams = {
            "name": "Renamed Segment",
        }
        segment = await resend.Segments.update_async(
            id="78261eea-8f8b-4381-83c6-79fa7120f1cf", params=params
        )
        assert segment["object"] == "segment"
        assert segment["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"

    async def test_update_segments_async_raises_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Segments.UpdateParams = {
            "name": "Renamed Segment",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Segments.update_async(
                id="78261eea-8f8b-4381-83c6-79fa7120f1cf", params=params
            )
