import resend
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendAutomations(ResendBaseTest):
    def test_automations_create(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Automations.CreateParams = {
            "name": "Welcome Sequence",
            "steps": [
                {
                    "key": "trigger_1",
                    "type": "trigger",
                    "config": {"event_name": "user.signed_up"},
                },
                {
                    "key": "email_1",
                    "type": "send_email",
                    "config": {"template": {"id": "tpl_123"}},
                },
            ],
            "connections": [
                {"from": "trigger_1", "to": "email_1"},
            ],
        }
        automation = resend.Automations.create(params)
        assert automation["object"] == "automation"
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_automations_create_with_status(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Automations.CreateParams = {
            "name": "Welcome Sequence",
            "status": "enabled",
            "steps": [
                {
                    "key": "trigger_1",
                    "type": "trigger",
                    "config": {"event_name": "user.signed_up"},
                },
            ],
            "connections": [],
        }
        automation = resend.Automations.create(params)
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_automations_get(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "name": "Welcome Sequence",
                "status": "enabled",
                "created_at": "2024-01-01T00:00:00.000Z",
                "updated_at": "2024-01-02T00:00:00.000Z",
                "steps": [
                    {
                        "key": "trigger_1",
                        "type": "trigger",
                        "config": {"event_name": "user.signed_up"},
                    }
                ],
                "connections": [],
            }
        )

        automation = resend.Automations.get("b6d24b8e-af0b-4c3c-be0c-359bbd97381e")
        assert automation["object"] == "automation"
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert automation["name"] == "Welcome Sequence"
        assert automation["status"] == "enabled"
        assert automation["created_at"] == "2024-01-01T00:00:00.000Z"
        assert automation["updated_at"] == "2024-01-02T00:00:00.000Z"
        assert len(automation["steps"]) == 1
        assert automation["steps"][0]["key"] == "trigger_1"
        assert automation["steps"][0]["type"] == "trigger"
        assert len(automation["connections"]) == 0

    def test_automations_update(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Automations.UpdateParams = {
            "automation_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            "status": "enabled",
        }
        automation = resend.Automations.update(params)
        assert automation["object"] == "automation"
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_automations_update_name(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Automations.UpdateParams = {
            "automation_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            "name": "Updated Sequence",
        }
        automation = resend.Automations.update(params)
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    def test_automations_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "deleted": True,
            }
        )

        resp = resend.Automations.remove("b6d24b8e-af0b-4c3c-be0c-359bbd97381e")
        assert resp["object"] == "automation"
        assert resp["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert resp["deleted"] is True

    def test_automations_stop(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "status": "disabled",
            }
        )

        resp = resend.Automations.stop("b6d24b8e-af0b-4c3c-be0c-359bbd97381e")
        assert resp["object"] == "automation"
        assert resp["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert resp["status"] == "disabled"

    def test_automations_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                        "name": "Welcome Sequence",
                        "status": "enabled",
                        "created_at": "2024-01-01T00:00:00.000Z",
                        "updated_at": "2024-01-02T00:00:00.000Z",
                    },
                    {
                        "id": "c7e35c9f-bf1c-5d4d-cf1d-460cce08492f",
                        "name": "Onboarding Flow",
                        "status": "disabled",
                        "created_at": "2024-02-01T00:00:00.000Z",
                        "updated_at": "2024-02-02T00:00:00.000Z",
                    },
                ],
            }
        )

        automations = resend.Automations.list()
        assert automations["object"] == "list"
        assert automations["has_more"] is False
        assert len(automations["data"]) == 2

        first = automations["data"][0]
        assert first["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert first["name"] == "Welcome Sequence"
        assert first["status"] == "enabled"
        assert first["created_at"] == "2024-01-01T00:00:00.000Z"

        second = automations["data"][1]
        assert second["id"] == "c7e35c9f-bf1c-5d4d-cf1d-460cce08492f"
        assert second["status"] == "disabled"

    def test_automations_list_with_status_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                        "name": "Welcome Sequence",
                        "status": "enabled",
                        "created_at": "2024-01-01T00:00:00.000Z",
                        "updated_at": "2024-01-02T00:00:00.000Z",
                    },
                ],
            }
        )

        params: resend.Automations.ListParams = {"status": "enabled"}
        automations = resend.Automations.list(params=params)
        assert automations["object"] == "list"
        assert len(automations["data"]) == 1
        assert automations["data"][0]["status"] == "enabled"

    def test_automations_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                        "name": "Welcome Sequence",
                        "status": "enabled",
                        "created_at": "2024-01-01T00:00:00.000Z",
                        "updated_at": "2024-01-02T00:00:00.000Z",
                    },
                ],
            }
        )

        params: resend.Automations.ListParams = {
            "limit": 10,
            "after": "some-cursor",
        }
        automations = resend.Automations.list(params=params)
        assert automations["has_more"] is True
        assert len(automations["data"]) == 1

    def test_automations_list_runs(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "run_123",
                        "status": "completed",
                        "started_at": "2024-01-01T10:00:00.000Z",
                        "completed_at": "2024-01-01T10:05:00.000Z",
                        "created_at": "2024-01-01T09:59:00.000Z",
                    },
                    {
                        "id": "run_456",
                        "status": "running",
                        "started_at": "2024-01-02T10:00:00.000Z",
                        "completed_at": None,
                        "created_at": "2024-01-02T09:59:00.000Z",
                    },
                ],
            }
        )

        runs = resend.Automations.Runs.list("b6d24b8e-af0b-4c3c-be0c-359bbd97381e")
        assert runs["object"] == "list"
        assert runs["has_more"] is False
        assert len(runs["data"]) == 2

        first = runs["data"][0]
        assert first["id"] == "run_123"
        assert first["status"] == "completed"
        assert first["started_at"] == "2024-01-01T10:00:00.000Z"
        assert first["completed_at"] == "2024-01-01T10:05:00.000Z"

        second = runs["data"][1]
        assert second["id"] == "run_456"
        assert second["status"] == "running"
        assert second["completed_at"] is None

    def test_automations_list_runs_with_status_filter(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "run_123",
                        "status": "completed",
                        "started_at": "2024-01-01T10:00:00.000Z",
                        "completed_at": "2024-01-01T10:05:00.000Z",
                        "created_at": "2024-01-01T09:59:00.000Z",
                    },
                ],
            }
        )

        params: resend.Automations.Runs.ListParams = {"status": "completed"}
        runs = resend.Automations.Runs.list(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e", params=params
        )
        assert len(runs["data"]) == 1
        assert runs["data"][0]["status"] == "completed"

    def test_automations_get_run(self) -> None:
        self.set_mock_json(
            {
                "object": "automation_run",
                "id": "run_123",
                "status": "completed",
                "started_at": "2024-01-01T10:00:00.000Z",
                "completed_at": "2024-01-01T10:05:00.000Z",
                "created_at": "2024-01-01T09:59:00.000Z",
                "steps": [
                    {
                        "key": "trigger_1",
                        "type": "trigger",
                        "status": "completed",
                        "started_at": "2024-01-01T10:00:00.000Z",
                        "completed_at": "2024-01-01T10:00:01.000Z",
                        "output": None,
                        "error": None,
                        "created_at": "2024-01-01T09:59:00.000Z",
                    },
                    {
                        "key": "email_1",
                        "type": "send_email",
                        "status": "completed",
                        "started_at": "2024-01-01T10:01:00.000Z",
                        "completed_at": "2024-01-01T10:01:02.000Z",
                        "output": None,
                        "error": None,
                        "created_at": "2024-01-01T09:59:00.000Z",
                    },
                ],
            }
        )

        run = resend.Automations.Runs.get(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e", "run_123"
        )
        assert run["object"] == "automation_run"
        assert run["id"] == "run_123"
        assert run["status"] == "completed"
        assert run["started_at"] == "2024-01-01T10:00:00.000Z"
        assert run["completed_at"] == "2024-01-01T10:05:00.000Z"
        assert len(run["steps"]) == 2
        assert run["steps"][0]["key"] == "trigger_1"
        assert run["steps"][0]["type"] == "trigger"
        assert run["steps"][0]["status"] == "completed"
        assert run["steps"][1]["key"] == "email_1"
        assert run["steps"][1]["type"] == "send_email"
