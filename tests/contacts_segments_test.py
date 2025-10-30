import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendContactSegments(ResendBaseTest):
    def test_contact_segments_add(self) -> None:
        self.set_mock_json({"id": "contact-segment-id-123"})

        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        response = resend.Contacts.Segments.add(params)
        assert response["id"] == "contact-segment-id-123"

    def test_contact_segments_add_with_email(self) -> None:
        self.set_mock_json({"id": "contact-segment-id-456"})

        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
            "email": "test@example.com",
        }
        response = resend.Contacts.Segments.add(params)
        assert response["id"] == "contact-segment-id-456"

    def test_contact_segments_add_raises_without_identifier(self) -> None:
        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
        }
        with self.assertRaises(ValueError) as context:
            resend.Contacts.Segments.add(params)
        assert "Either contact_id or email must be provided" in str(context.exception)

    def test_contact_segments_remove(self) -> None:
        self.set_mock_json({"id": "contact-segment-id-123", "deleted": True})

        params: resend.ContactSegments.RemoveParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        response = resend.Contacts.Segments.remove(params)
        assert response["id"] == "contact-segment-id-123"
        assert response["deleted"] is True

    def test_contact_segments_remove_with_email(self) -> None:
        self.set_mock_json({"id": "contact-segment-id-456", "deleted": True})

        params: resend.ContactSegments.RemoveParams = {
            "segment_id": "segment-123",
            "email": "test@example.com",
        }
        response = resend.Contacts.Segments.remove(params)
        assert response["id"] == "contact-segment-id-456"
        assert response["deleted"] is True

    def test_contact_segments_remove_raises_without_identifier(self) -> None:
        params: resend.ContactSegments.RemoveParams = {
            "segment_id": "segment-123",
        }
        with self.assertRaises(ValueError) as context:
            resend.Contacts.Segments.remove(params)
        assert "Either contact_id or email must be provided" in str(context.exception)

    def test_contact_segments_list(self) -> None:
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
            resend.Contacts.Segments.list(params)
        )
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert len(response["data"]) == 2
        assert response["data"][0]["id"] == "segment-1"
        assert response["data"][1]["id"] == "segment-2"

    def test_contact_segments_list_with_email(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "segment-3",
                        "name": "Segment 3",
                        "created_at": "2023-10-08T22:59:55.977Z",
                    }
                ],
            }
        )

        params: resend.ContactSegments.ListParams = {
            "email": "test@example.com",
        }
        response = resend.Contacts.Segments.list(params)
        assert response["object"] == "list"
        assert response["has_more"] is False
        assert len(response["data"]) == 1
        assert response["data"][0]["id"] == "segment-3"

    def test_contact_segments_list_with_pagination(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "segment-4",
                        "name": "Segment 4",
                        "created_at": "2023-10-09T22:59:55.977Z",
                    }
                ],
            }
        )

        params: resend.ContactSegments.ListParams = {
            "contact_id": "contact-123",
        }
        pagination: resend.ContactSegments.ListContactSegmentsParams = {
            "limit": 10,
            "after": "segment-3",
        }
        response = resend.Contacts.Segments.list(params, pagination)
        assert response["object"] == "list"
        assert response["has_more"] is True
        assert len(response["data"]) == 1

    def test_contact_segments_list_raises_without_identifier(self) -> None:
        params: resend.ContactSegments.ListParams = {}
        with self.assertRaises(ValueError) as context:
            resend.Contacts.Segments.list(params)
        assert "Either contact_id or email must be provided" in str(context.exception)

    def test_should_add_contact_segments_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.ContactSegments.AddParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.Segments.add(params)

    def test_should_remove_contact_segments_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactSegments.RemoveParams = {
            "segment_id": "segment-123",
            "contact_id": "contact-456",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.Segments.remove(params)

    def test_should_list_contact_segments_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.ContactSegments.ListParams = {
            "contact_id": "contact-123",
        }
        with self.assertRaises(NoContentError):
            _ = resend.Contacts.Segments.list(params)
