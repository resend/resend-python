import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendSegments(ResendBaseTest):
    def test_segments_create(self) -> None:
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
        segment = resend.Segments.create(params)
        assert segment["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert segment["name"] == "Registered Users"

    def test_should_create_segments_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Segments.CreateParams = {
            "name": "Python SDK Segment",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Segments.create(params)

    def test_segments_get(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "Registered Users",
                "created_at": "2023-10-06T22:59:55.977Z",
            }
        )

        segment = resend.Segments.get(id="78261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert segment["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert segment["name"] == "Registered Users"
        assert segment["created_at"] == "2023-10-06T22:59:55.977Z"

    def test_should_get_segments_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Segments.get(id="78261eea-8f8b-4381-83c6-79fa7120f1cf")

    def test_segments_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "audience",
                "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        rmed: resend.Segments.RemoveSegmentResponse = resend.Segments.remove(
            "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        )
        assert rmed["object"] == "audience"
        assert rmed["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert rmed["deleted"] is True

    def test_should_remove_segments_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Segments.remove(id="78261eea-8f8b-4381-83c6-79fa7120f1cf")

    def test_segments_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "name": "Registered Users",
                        "created_at": "2023-10-06T22:59:55.977Z",
                    }
                ],
            }
        )

        segments: resend.Segments.ListResponse = resend.Segments.list()
        assert segments["object"] == "list"
        assert segments["has_more"] is False
        assert segments["data"][0]["id"] == "78261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert segments["data"][0]["name"] == "Registered Users"

    def test_should_list_segments_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Segments.list()

    def test_segments_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "segment-1",
                        "name": "First Segment",
                        "created_at": "2023-10-06T22:59:55.977Z",
                    },
                    {
                        "id": "segment-2",
                        "name": "Second Segment",
                        "created_at": "2023-10-07T22:59:55.977Z",
                    },
                ],
            }
        )

        params: resend.Segments.ListParams = {
            "limit": 10,
            "after": "previous-segment-id",
        }
        segments: resend.Segments.ListResponse = resend.Segments.list(params=params)
        assert segments["object"] == "list"
        assert segments["has_more"] is True
        assert len(segments["data"]) == 2
        assert segments["data"][0]["id"] == "segment-1"
        assert segments["data"][1]["id"] == "segment-2"

    def test_segments_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "segment-3",
                        "name": "Third Segment",
                        "created_at": "2023-10-05T22:59:55.977Z",
                    }
                ],
            }
        )

        params: resend.Segments.ListParams = {
            "limit": 5,
            "before": "later-segment-id",
        }
        segments: resend.Segments.ListResponse = resend.Segments.list(params=params)
        assert segments["object"] == "list"
        assert segments["has_more"] is False
        assert len(segments["data"]) == 1
        assert segments["data"][0]["id"] == "segment-3"
