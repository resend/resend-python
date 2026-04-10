import resend
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendEvents(ResendBaseTest):
    def test_events_create(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        params: resend.Events.CreateParams = {
            "name": "user.signed_up",
        }
        event = resend.Events.create(params)
        assert event["object"] == "event"
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"

    def test_events_create_with_schema(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        params: resend.Events.CreateParams = {
            "name": "user.signed_up",
            "schema": {
                "plan": "string",
                "trial_days": "number",
                "is_enterprise": "boolean",
            },
        }
        event = resend.Events.create(params)
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"

    def test_events_get_by_id(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "user.signed_up",
                "schema": {"plan": "string"},
                "created_at": "2024-01-01T00:00:00.000Z",
                "updated_at": None,
            }
        )

        event = resend.Events.get("56261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert event["object"] == "event"
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert event["name"] == "user.signed_up"
        assert event["schema"] == {"plan": "string"}
        assert event["created_at"] == "2024-01-01T00:00:00.000Z"
        assert event["updated_at"] is None

    def test_events_get_by_name(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                "name": "user.signed_up",
                "schema": None,
                "created_at": "2024-01-01T00:00:00.000Z",
                "updated_at": None,
            }
        )

        event = resend.Events.get("user.signed_up")
        assert event["name"] == "user.signed_up"
        assert event["schema"] is None

    def test_events_update(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        params: resend.Events.UpdateParams = {
            "identifier": "user.signed_up",
            "schema": {"plan": "string", "amount": "number"},
        }
        event = resend.Events.update(params)
        assert event["object"] == "event"
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"

    def test_events_update_clear_schema(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
            }
        )

        params: resend.Events.UpdateParams = {
            "identifier": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
            "schema": None,
        }
        event = resend.Events.update(params)
        assert event["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"

    def test_events_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        resp = resend.Events.remove("56261eea-8f8b-4381-83c6-79fa7120f1cf")
        assert resp["object"] == "event"
        assert resp["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert resp["deleted"] is True

    def test_events_remove_by_name(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                "deleted": True,
            }
        )

        resp = resend.Events.remove("user.signed_up")
        assert resp["deleted"] is True

    def test_events_send_with_contact_id(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "event": "user.signed_up",
            }
        )

        params: resend.Events.SendParams = {
            "event": "user.signed_up",
            "contact_id": "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e",
        }
        resp = resend.Events.send(params)
        assert resp["object"] == "event"
        assert resp["event"] == "user.signed_up"

    def test_events_send_with_email(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "event": "user.signed_up",
            }
        )

        params: resend.Events.SendParams = {
            "event": "user.signed_up",
            "email": "user@example.com",
        }
        resp = resend.Events.send(params)
        assert resp["event"] == "user.signed_up"

    def test_events_send_with_payload(self) -> None:
        self.set_mock_json(
            {
                "object": "event",
                "event": "user.signed_up",
            }
        )

        params: resend.Events.SendParams = {
            "event": "user.signed_up",
            "email": "user@example.com",
            "payload": {"plan": "pro", "trial_days": 14},
        }
        resp = resend.Events.send(params)
        assert resp["event"] == "user.signed_up"

    def test_events_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "name": "user.signed_up",
                        "schema": {"plan": "string"},
                        "created_at": "2024-01-01T00:00:00.000Z",
                        "updated_at": None,
                    },
                    {
                        "id": "67372ffb-9g9c-5492-94d7-80gb8231g2dg",
                        "name": "user.upgraded",
                        "schema": None,
                        "created_at": "2024-02-01T00:00:00.000Z",
                        "updated_at": "2024-02-15T00:00:00.000Z",
                    },
                ],
            }
        )

        events = resend.Events.list()
        assert events["object"] == "list"
        assert events["has_more"] is False
        assert len(events["data"]) == 2

        first = events["data"][0]
        assert first["id"] == "56261eea-8f8b-4381-83c6-79fa7120f1cf"
        assert first["name"] == "user.signed_up"
        assert first["schema"] == {"plan": "string"}
        assert first["updated_at"] is None

        second = events["data"][1]
        assert second["name"] == "user.upgraded"
        assert second["schema"] is None
        assert second["updated_at"] == "2024-02-15T00:00:00.000Z"

    def test_events_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "56261eea-8f8b-4381-83c6-79fa7120f1cf",
                        "name": "user.signed_up",
                        "schema": None,
                        "created_at": "2024-01-01T00:00:00.000Z",
                        "updated_at": None,
                    }
                ],
            }
        )

        params: resend.Events.ListParams = {
            "limit": 10,
            "after": "some-cursor",
        }
        events = resend.Events.list(params=params)
        assert events["has_more"] is True
        assert len(events["data"]) == 1
