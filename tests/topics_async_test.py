import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendTopicsAsync(AsyncResendBaseTest):
    async def test_topics_create_async(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Topics.CreateParams = {
            "name": "Weekly Newsletter",
            "default_subscription": "opt_in",
        }
        topic = await resend.Topics.create_async(params)
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    async def test_should_create_topics_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Topics.CreateParams = {
            "name": "Weekly Newsletter",
            "default_subscription": "opt_in",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Topics.create_async(params)

    async def test_topics_get_async(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "name": "Weekly Newsletter",
                "description": "Weekly newsletter for our subscribers",
                "default_subscription": "opt_in",
                "created_at": "2023-04-08T00:11:13.110779+00:00",
            }
        )

        topic = await resend.Topics.get_async(id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e")
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert topic["name"] == "Weekly Newsletter"

    async def test_should_get_topics_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Topics.get_async(id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e")

    async def test_topics_update_async(self) -> None:
        self.set_mock_json(
            {
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        )

        params: resend.Topics.UpdateParams = {
            "name": "Monthly Newsletter",
            "description": "Monthly newsletter for our subscribers",
        }
        topic = await resend.Topics.update_async(
            id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e", params=params
        )
        assert topic["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    async def test_should_update_topics_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Topics.UpdateParams = {
            "name": "Monthly Newsletter",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Topics.update_async(
                id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e", params=params
            )

    async def test_topics_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "topic",
                "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                "deleted": True,
            }
        )

        removed = await resend.Topics.remove_async(
            "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        )
        assert removed["object"] == "topic"
        assert removed["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
        assert removed["deleted"] is True

    async def test_should_remove_topics_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Topics.remove_async(
                id="b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
            )

    async def test_topics_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
                        "name": "Weekly Newsletter",
                        "description": "Weekly newsletter for our subscribers",
                        "default_subscription": "opt_in",
                        "created_at": "2023-04-08T00:11:13.110779+00:00",
                    }
                ],
            }
        )

        topics: resend.Topics.ListResponse = await resend.Topics.list_async()
        assert topics["object"] == "list"
        assert topics["has_more"] is False
        assert topics["data"][0]["id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"

    async def test_should_list_topics_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Topics.list_async()
