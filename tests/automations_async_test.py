import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendAutomationsAsync(AsyncResendBaseTest):
    async def test_automations_create_async(self) -> None:
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
            ],
            "connections": [],
        }
        automation = await resend.Automations.create_async(params)
        assert automation["object"] == "automation"
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    async def test_automations_create_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Automations.CreateParams = {
            "name": "Welcome Sequence",
            "steps": [
                {
                    "key": "trigger_1",
                    "type": "trigger",
                    "config": {"event_name": "user.signed_up"},
                },
            ],
            "connections": [],
        }
        with pytest.raises(NoContentError):
            _ = await resend.Automations.create_async(params)

    async def test_automations_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "name": "Welcome Sequence",
                "status": "enabled",
                "created_at": "2024-01-01T00:00:00.000Z",
                "updated_at": "2024-01-02T00:00:00.000Z",
                "steps": [],
                "connections": [],
            }
        )

        automation = await resend.Automations.get_async(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        )
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert automation["name"] == "Welcome Sequence"
        assert automation["status"] == "enabled"

    async def test_automations_get_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Automations.get_async(
                "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
            )

    async def test_automations_update_async(self) -> None:
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
        automation = await resend.Automations.update_async(params)
        assert automation["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    async def test_automations_update_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Automations.UpdateParams = {
            "automation_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            "status": "enabled",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Automations.update_async(params)

    async def test_automations_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "deleted": True,
            }
        )

        resp = await resend.Automations.remove_async(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        )
        assert resp["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert resp["deleted"] is True

    async def test_automations_remove_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Automations.remove_async(
                "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
            )

    async def test_automations_stop_async(self) -> None:
        self.set_mock_json(
            {
                "object": "automation",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "status": "disabled",
            }
        )

        resp = await resend.Automations.stop_async(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        )
        assert resp["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert resp["status"] == "disabled"

    async def test_automations_stop_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Automations.stop_async(
                "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
            )

    async def test_automations_list_async(self) -> None:
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

        automations = await resend.Automations.list_async()
        assert automations["object"] == "list"
        assert automations["has_more"] is False
        assert len(automations["data"]) == 1
        assert automations["data"][0]["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    async def test_automations_list_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Automations.list_async()

    async def test_automations_list_runs_async(self) -> None:
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

        runs = await resend.Automations.Runs.list_async(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        )
        assert runs["object"] == "list"
        assert len(runs["data"]) == 1
        assert runs["data"][0]["id"] == "run_123"
        assert runs["data"][0]["status"] == "completed"

    async def test_automations_list_runs_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Automations.Runs.list_async(
                "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
            )

    async def test_automations_get_run_async(self) -> None:
        self.set_mock_json(
            {
                "object": "automation_run",
                "id": "run_123",
                "status": "completed",
                "started_at": "2024-01-01T10:00:00.000Z",
                "completed_at": "2024-01-01T10:05:00.000Z",
                "created_at": "2024-01-01T09:59:00.000Z",
                "steps": [],
            }
        )

        run = await resend.Automations.Runs.get_async(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e", "run_123"
        )
        assert run["object"] == "automation_run"
        assert run["id"] == "run_123"
        assert run["status"] == "completed"

    async def test_automations_get_run_async_raises_when_no_content(self) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Automations.Runs.get_async(
                "b6d24b8e-af0b-4c3c-be0c-359bbd97381e", "run_123"
            )
