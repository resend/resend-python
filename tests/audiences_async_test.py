import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendSegmentsAsync(AsyncResendBaseTest):
    async def test_segments_create_async(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
            }
        )

        params: resend.Segments.CreateParams = {
            "name": "Python SDK Segment",
        }
        segment = await resend.Segments.create_async(params)
        assert segment["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert segment["name"] == "Registered Users"

    async def test_should_create_segments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Segments.CreateParams = {
            "name": "Python SDK Segment",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Segments.create_async(params)

    async def test_segments_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
                "created_at": "2023-10-06T22:59:55.977Z",
            }
        )

        segment = await resend.Segments.get_async(
            id="78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert segment["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert segment["name"] == "Registered Users"
        assert segment["created_at"] == "2023-10-06T22:59:55.977Z"

    async def test_should_get_segments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Segments.get_async(
                id="78261eea-8f8b-4381-83c6-79fa7120f1cf"
            )

    async def test_segments_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        rmed = await resend.Segments.remove_async(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

    async def test_should_remove_segments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Segments.remove_async(
                id="78261eea-8f8b-4381-83c6-79fa7120f1cf"
            )

    async def test_segments_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "data": [
                    {
                        "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "name": "Registered Users",
                        "created_at": "2023-10-06T22:59:55.977Z",
                    }
                ],
            }
        )

        segments: resend.Segments.ListResponse = await resend.Segments.list_async()
        assert segments["data"][0]["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert segments["data"][0]["name"] == "Registered Users"

    async def test_should_list_segments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Segments.list_async()
