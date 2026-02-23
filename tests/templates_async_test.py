import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendTemplatesAsync(AsyncResendBaseTest):
    async def test_templates_create_async(self) -> None:
        self.set_mock_json(
            {"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794", "object": "template"}
        )

        params: resend.Templates.CreateParams = {
            "name": "welcome-email",
            "html": "<strong>Hey, {{{NAME}}}, you are {{{AGE}}} years old.</strong>",
            "variables": [
                {
                    "key": "NAME",
                    "type": "string",
                    "fallback_value": "user",
                },
                {
                    "key": "AGE",
                    "type": "number",
                    "fallback_value": 25,
                },
            ],
        }
        template: resend.Templates.CreateResponse = await resend.Templates.create_async(
            params
        )
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"

    async def test_should_create_templates_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Templates.CreateParams = {
            "name": "welcome-email",
            "html": "<strong>Hello</strong>",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Templates.create_async(params)

    async def test_templates_get_async(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
                "object": "template",
                "name": "welcome-email",
                "alias": "welcome",
                "from": "Acme <onboarding@example.com>",
                "subject": "Welcome to Acme!",
                "reply_to": "support@example.com",
                "html": "<strong>Hey, {{{NAME}}}, you are {{{AGE}}} years old.</strong>",
                "text": "Hey, {{{NAME}}}, you are {{{AGE}}} years old.",
                "variables": [
                    {
                        "key": "NAME",
                        "type": "string",
                        "fallback_value": "user",
                    },
                    {
                        "key": "AGE",
                        "type": "number",
                        "fallback_value": 25,
                    },
                ],
                "created_at": "2024-01-15T10:30:00.000Z",
                "updated_at": "2024-01-15T10:30:00.000Z",
                "published_at": "2024-01-15T11:00:00.000Z",
            }
        )

        template = await resend.Templates.get_async(
            "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"
        assert template["name"] == "welcome-email"

    async def test_should_get_templates_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Templates.get_async("49a3999c-0ce1-4ea6-ab68-afcd6dc2e794")

    async def test_templates_update_async(self) -> None:
        self.set_mock_json(
            {"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794", "object": "template"}
        )

        params: resend.Templates.UpdateParams = {
            "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            "name": "updated-welcome-email",
            "html": "<strong>Welcome, {{{NAME}}}!</strong>",
        }
        template: resend.Templates.UpdateResponse = await resend.Templates.update_async(
            params
        )
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"

    async def test_should_update_templates_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Templates.UpdateParams = {
            "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            "name": "updated-welcome-email",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Templates.update_async(params)

    async def test_templates_publish_async(self) -> None:
        self.set_mock_json(
            {"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794", "object": "template"}
        )

        template: resend.Templates.PublishResponse = (
            await resend.Templates.publish_async("49a3999c-0ce1-4ea6-ab68-afcd6dc2e794")
        )
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"

    async def test_should_publish_templates_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Templates.publish_async(
                "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
            )

    async def test_templates_duplicate_async(self) -> None:
        self.set_mock_json(
            {"id": "e169aa45-1ecf-4183-9955-b1499d5701d3", "object": "template"}
        )

        duplicated: resend.Templates.DuplicateResponse = (
            await resend.Templates.duplicate_async(
                "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
            )
        )
        assert duplicated["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert duplicated["object"] == "template"

    async def test_should_duplicate_templates_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Templates.duplicate_async(
                "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
            )

    async def test_templates_remove_async(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
                "object": "template",
                "deleted": True,
            }
        )

        response: resend.Templates.RemoveResponse = await resend.Templates.remove_async(
            "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )
        assert response["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert response["object"] == "template"
        assert response["deleted"] is True

    async def test_should_remove_templates_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Templates.remove_async(
                "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
            )

    async def test_templates_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "template-1",
                        "name": "welcome-email",
                        "status": "published",
                        "published_at": "2024-01-15T11:00:00.000Z",
                        "created_at": "2024-01-15T10:30:00.000Z",
                        "updated_at": "2024-01-15T10:30:00.000Z",
                        "alias": "welcome",
                    }
                ],
            }
        )

        templates: resend.Templates.ListResponse = await resend.Templates.list_async()
        assert templates["object"] == "list"
        assert templates["has_more"] is False
        assert len(templates["data"]) == 1
        assert templates["data"][0]["id"] == "template-1"

    async def test_should_list_templates_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Templates.list_async()
