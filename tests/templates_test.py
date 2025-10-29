import resend
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendTemplates(ResendBaseTest):
    def test_templates_create(self) -> None:
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
        template: resend.Templates.CreateResponse = resend.Templates.create(params)
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"

    def test_templates_create_with_optional_fields(self) -> None:
        self.set_mock_json(
            {"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794", "object": "template"}
        )

        params: resend.Templates.CreateParams = {
            "name": "welcome-email",
            "alias": "welcome",
            "from": "Acme <onboarding@example.com>",
            "subject": "Welcome to Acme!",
            "reply_to": "support@example.com",
            "html": "<strong>Welcome, {{{NAME}}}!</strong>",
            "text": "Welcome, {{{NAME}}}!",
            "variables": [
                {
                    "key": "NAME",
                    "type": "string",
                    "fallback_value": "user",
                }
            ],
        }
        template: resend.Templates.CreateResponse = resend.Templates.create(params)
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"

    def test_templates_get(self) -> None:
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

        template = resend.Templates.get("49a3999c-0ce1-4ea6-ab68-afcd6dc2e794")
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"
        assert template["name"] == "welcome-email"
        assert template["alias"] == "welcome"
        assert template["from"] == "Acme <onboarding@example.com>"
        assert template["subject"] == "Welcome to Acme!"
        assert template["reply_to"] == "support@example.com"
        assert (
            template["html"]
            == "<strong>Hey, {{{NAME}}}, you are {{{AGE}}} years old.</strong>"
        )
        assert template["text"] == "Hey, {{{NAME}}}, you are {{{AGE}}} years old."
        assert len(template["variables"]) == 2
        assert template["variables"][0]["key"] == "NAME"
        assert template["variables"][0]["type"] == "string"
        assert template["variables"][0]["fallback_value"] == "user"
        assert template["variables"][1]["key"] == "AGE"
        assert template["variables"][1]["type"] == "number"
        assert template["variables"][1]["fallback_value"] == 25
        assert template["created_at"] == "2024-01-15T10:30:00.000Z"
        assert template["updated_at"] == "2024-01-15T10:30:00.000Z"
        assert template["published_at"] == "2024-01-15T11:00:00.000Z"

    def test_templates_update(self) -> None:
        self.set_mock_json(
            {"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794", "object": "template"}
        )

        params: resend.Templates.UpdateParams = {
            "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            "name": "updated-welcome-email",
            "html": "<strong>Welcome, {{{NAME}}}!</strong>",
        }
        template: resend.Templates.UpdateResponse = resend.Templates.update(params)
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"

    def test_templates_publish(self) -> None:
        self.set_mock_json(
            {"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794", "object": "template"}
        )

        template: resend.Templates.PublishResponse = resend.Templates.publish(
            "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"

    def test_templates_duplicate(self) -> None:
        self.set_mock_json(
            {"id": "e169aa45-1ecf-4183-9955-b1499d5701d3", "object": "template"}
        )

        duplicated: resend.Templates.DuplicateResponse = resend.Templates.duplicate(
            "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )
        assert duplicated["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert duplicated["object"] == "template"

    def test_templates_remove(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
                "object": "template",
                "deleted": True,
            }
        )

        response: resend.Templates.RemoveResponse = resend.Templates.remove(
            "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        )
        assert response["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert response["object"] == "template"
        assert response["deleted"] is True

    def test_templates_list(self) -> None:
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
                    },
                    {
                        "id": "template-2",
                        "name": "goodbye-email",
                        "status": "draft",
                        "published_at": None,
                        "created_at": "2024-01-16T10:30:00.000Z",
                        "updated_at": "2024-01-16T10:30:00.000Z",
                        "alias": "goodbye",
                    },
                ],
            }
        )

        templates: resend.Templates.ListResponse = resend.Templates.list()
        assert templates["object"] == "list"
        assert templates["has_more"] is False
        assert len(templates["data"]) == 2

        template = templates["data"][0]
        assert template["id"] == "template-1"
        assert template["name"] == "welcome-email"
        assert template["status"] == "published"
        assert template["published_at"] == "2024-01-15T11:00:00.000Z"
        assert template["created_at"] == "2024-01-15T10:30:00.000Z"
        assert template["updated_at"] == "2024-01-15T10:30:00.000Z"
        assert template["alias"] == "welcome"

        template = templates["data"][1]
        assert template["id"] == "template-2"
        assert template["name"] == "goodbye-email"
        assert template["status"] == "draft"
        assert template["published_at"] is None
        assert template["created_at"] == "2024-01-16T10:30:00.000Z"
        assert template["updated_at"] == "2024-01-16T10:30:00.000Z"
        assert template["alias"] == "goodbye"

    def test_templates_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
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

        params: resend.Templates.ListParams = {
            "limit": 10,
            "after": "previous-template-id",
        }
        templates: resend.Templates.ListResponse = resend.Templates.list(params=params)
        assert templates["object"] == "list"
        assert templates["has_more"] is True
        assert len(templates["data"]) == 1
        assert templates["data"][0]["id"] == "template-1"

    def test_templates_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "template-3",
                        "name": "password-reset",
                        "status": "draft",
                        "published_at": None,
                        "created_at": "2024-01-14T10:30:00.000Z",
                        "updated_at": "2024-01-14T10:30:00.000Z",
                        "alias": "password-reset",
                    }
                ],
            }
        )

        params: resend.Templates.ListParams = {
            "limit": 5,
            "before": "later-template-id",
        }
        templates: resend.Templates.ListResponse = resend.Templates.list(params=params)
        assert templates["object"] == "list"
        assert templates["has_more"] is False
        assert len(templates["data"]) == 1
        assert templates["data"][0]["id"] == "template-3"

    def test_templates_variable_types(self) -> None:
        """Test that various variable types are properly supported."""
        self.set_mock_json(
            {"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794", "object": "template"}
        )

        params: resend.Templates.CreateParams = {
            "name": "complex-template",
            "html": "<div>{{{STRING}}} {{{NUMBER}}} {{{AGE}}} {{{SCORE}}}</div>",
            "variables": [
                {
                    "key": "STRING",
                    "type": "string",
                    "fallback_value": "default",
                },
                {
                    "key": "NUMBER",
                    "type": "number",
                    "fallback_value": 42,
                },
                {
                    "key": "AGE",
                    "type": "number",
                    "fallback_value": 25,
                },
                {
                    "key": "SCORE",
                    "type": "number",
                    "fallback_value": 100,
                },
            ],
        }
        template: resend.Templates.CreateResponse = resend.Templates.create(params)
        assert template["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        assert template["object"] == "template"
