import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendContactSegmentsAsync(ResendBaseTest):
    async def test_contact_segments_add_async(self) -> None:
        self.set_mock_json({"id": "contact-segment-id-123"})

        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        response = await resend.Contacts.Segments.add_async(params)
        assert response["id"] == "contact-segment-id-123"

    async def test_contact_segments_add_async_with_email(self) -> None:
        self.set_mock_json({"id": "contact-segment-id-456"})

        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
            "email": "test@example.com",
        }
        response = await resend.Contacts.Segments.add_async(params)
        assert response["id"] == "contact-segment-id-456"

    async def test_contact_segments_add_async_raises_without_identifier(self) -> None:
        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
        }
        with self.assertRaises(ValueError) as context:
            await resend.Contacts.Segments.add_async(params)
        assert "Either contact_id or email must be provided" in str(context.exception)

    async def test_should_add_contact_segments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        with self.assertRaises(NoContentError):
            _ = await resend.Contacts.Segments.add_async(params)

    async def test_contact_segments_remove_async(self) -> None:
        self.set_mock_json({"id": "contact-segment-id-123", "deleted": True})

        params: resend.ContactSegments.RemoveParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        response = await resend.Contacts.Segments.remove_async(params)
        assert response["id"] == "contact-segment-id-123"
        assert response["deleted"] is True

    async def test_contact_segments_remove_async_raises_without_identifier(
        self,
    ) -> None:
        params: resend.ContactSegments.RemoveParams = {
            "segment_id": "segment-123",
        }
        with self.assertRaises(ValueError) as context:
            await resend.Contacts.Segments.remove_async(params)
        assert "Either contact_id or email must be provided" in str(context.exception)

    async def test_should_remove_contact_segments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactSegments.RemoveParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        with self.assertRaises(NoContentError):
            _ = await resend.Contacts.Segments.remove_async(params)

    async def test_contact_segments_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "segment-1",
                        "name": "Segment 1",
                        "created_at": "2023-10-06T22:59:55.977Z",
                    },
                    {
                        "id": "segment-2",
                        "name": "Segment 2",
                        "created_at": "2023-10-07T22:59:55.977Z",
                    },
                ],
            }
        )

        params: resend.ContactSegments.ListParams = {
            "contact_id": "contact-123",
        }
        response: resend.ContactSegments.ListContactSegmentsResponse = (
            await resend.Contacts.Segments.list_async(params)
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert len(response["data"]) == 2
        assert response["data"][0]["id"] == "segment-1"
        assert response["data"][1]["id"] == "segment-2"

    async def test_contact_segments_list_async_raises_without_identifier(self) -> None:
        params: resend.ContactSegments.ListParams = {}
        with self.assertRaises(ValueError) as context:
            await resend.Contacts.Segments.list_async(params)
        assert "Either contact_id or email must be provided" in str(context.exception)

    async def test_should_list_contact_segments_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactSegments.ListParams = {
            "contact_id": "contact-123",
        }
        with self.assertRaises(NoContentError):
            _ = await resend.Contacts.Segments.list_async(params)
