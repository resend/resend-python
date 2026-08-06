from typing import Any, Dict, cast
from unittest.mock import AsyncMock

import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestSuppressionsAsync(AsyncResendBaseTest):
    async def test_suppressions_add_async(self) -> None:
        self.set_mock_json(
            {
                "object": "suppression",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
            }
        )

        params: resend.Suppressions.AddParams = {"email": "blocked@example.com"}
        added = await resend.Suppressions.add_async(params)
        assert added["object"] == "suppression"
        assert added["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"

    async def test_should_add_suppression_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Suppressions.AddParams = {"email": "blocked@example.com"}
        with pytest.raises(NoContentError):
            _ = await resend.Suppressions.add_async(params)

    async def test_suppressions_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "email": "bounced@example.com",
                        "origin": "bounce",
                        "source_id": "479e3145-dd38-476b-932c-529ceb705947",
                        "created_at": "2023-10-06 23:47:56.678+00",
                    },
                    {
                        "id": "fd61172c-cafc-40f5-b049-b45947779a29",
                        "email": "manual@example.com",
                        "origin": "manual",
                        "source_id": None,
                        "created_at": "2023-10-07 23:47:56.678+00",
                    },
                ],
            }
        )

        suppressions = await resend.Suppressions.list_async()
        assert suppressions["object"] == "list"
        assert suppressions["has_more"] is False
        assert suppressions["data"][0]["origin"] == "bounce"
        assert (
            suppressions["data"][0]["source_id"]
            == "479e3145-dd38-476b-932c-529ceb705947"
        )
        assert suppressions["data"][1]["source_id"] is None
        assert "object" not in suppressions["data"][0]

    async def test_suppressions_list_async_with_params(self) -> None:
        self.set_mock_json({"object": "list", "has_more": False, "data": []})

        params: resend.Suppressions.ListParams = {
            "origin": "complaint",
            "limit": 25,
        }
        suppressions = await resend.Suppressions.list_async(params)
        assert suppressions["has_more"] is False
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/suppressions?origin=complaint&limit=25"
        )

    async def test_should_list_suppressions_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Suppressions.list_async()

    async def test_suppressions_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "suppression",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "email": "bounced@example.com",
                "origin": "bounce",
                "source_id": "479e3145-dd38-476b-932c-529ceb705947",
                "created_at": "2023-10-06 23:47:56.678+00",
            }
        )

        suppression = await resend.Suppressions.get_async(
            "e169aa45-1ecf-4183-9955-b1499d5701d3"
        )
        assert suppression["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert suppression["email"] == "bounced@example.com"
        assert suppression["source_id"] == "479e3145-dd38-476b-932c-529ceb705947"

    async def test_suppressions_get_async_with_null_source_id(self) -> None:
        self.set_mock_json(
            {
                "object": "suppression",
                "id": "fd61172c-cafc-40f5-b049-b45947779a29",
                "email": "manual@example.com",
                "origin": "manual",
                "source_id": None,
                "created_at": "2023-10-06 23:47:56.678+00",
            }
        )

        suppression = await resend.Suppressions.get_async("manual@example.com")
        assert suppression["origin"] == "manual"
        assert suppression["source_id"] is None

    async def test_suppressions_get_async_encodes_email_identifier(self) -> None:
        self.set_mock_json(
            {
                "object": "suppression",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "email": "user+tag@example.com",
                "origin": "manual",
                "source_id": None,
                "created_at": "2023-10-06 23:47:56.678+00",
            }
        )

        suppression = await resend.Suppressions.get_async("user+tag@example.com")
        assert suppression["email"] == "user+tag@example.com"
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/suppressions/user%2Btag%40example.com"
        )

    async def test_suppressions_get_async_raises_without_identifier(self) -> None:
        with pytest.raises(ValueError):
            _ = await resend.Suppressions.get_async("")

    async def test_should_get_suppression_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Suppressions.get_async(
                "e169aa45-1ecf-4183-9955-b1499d5701d3"
            )

    async def test_suppressions_remove_async(self) -> None:
        self.set_mock_json(
            {
                "object": "suppression",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "deleted": True,
            }
        )

        removed = await resend.Suppressions.remove_async("blocked@example.com")
        assert removed["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert removed["deleted"] is True
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/suppressions/blocked%40example.com"
        )

    async def test_suppressions_remove_async_raises_without_identifier(self) -> None:
        with pytest.raises(ValueError):
            _ = await resend.Suppressions.remove_async("")

    async def test_should_remove_suppression_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Suppressions.remove_async("blocked@example.com")

    async def test_suppressions_batch_add_async(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {
                        "object": "suppression",
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                    },
                    {
                        "object": "suppression",
                        "id": "fd61172c-cafc-40f5-b049-b45947779a29",
                    },
                ]
            }
        )

        params: resend.Suppressions.Batch.AddParams = {
            "emails": ["one@example.com", "two@example.com"],
        }
        added = await resend.Suppressions.Batch.add_async(params)
        assert len(added["data"]) == 2
        assert added["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"

    async def test_suppressions_batch_add_async_dedupes_server_side(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {
                        "object": "suppression",
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                    }
                ]
            }
        )

        params: resend.Suppressions.Batch.AddParams = {
            "emails": ["ONE@example.com", "one@example.com", " one@example.com "],
        }
        added = await resend.Suppressions.Batch.add_async(params)
        assert len(added["data"]) == 1

    async def test_should_batch_add_suppressions_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Suppressions.Batch.AddParams = {"emails": ["one@example.com"]}
        with pytest.raises(NoContentError):
            _ = await resend.Suppressions.Batch.add_async(params)

    async def test_suppressions_batch_remove_async_with_emails(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {
                        "object": "suppression",
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "deleted": True,
                    }
                ]
            }
        )

        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
        }
        removed = await resend.Suppressions.Batch.remove_async(params)
        assert removed["data"][0]["deleted"] is True

    async def test_suppressions_batch_remove_async_with_ids(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {
                        "object": "suppression",
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "deleted": True,
                    },
                    {
                        "object": "suppression",
                        "id": "fd61172c-cafc-40f5-b049-b45947779a29",
                        "deleted": True,
                    },
                ]
            }
        )

        params: resend.Suppressions.Batch.RemoveParams = {
            "ids": [
                "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "fd61172c-cafc-40f5-b049-b45947779a29",
            ],
        }
        removed = await resend.Suppressions.Batch.remove_async(params)
        assert len(removed["data"]) == 2
        assert removed["data"][1]["deleted"] is True

    async def test_suppressions_batch_remove_async_omits_identifiers_not_suppressed(
        self,
    ) -> None:
        self.set_mock_json(
            {
                "data": [
                    {
                        "object": "suppression",
                        "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                        "deleted": True,
                    }
                ]
            }
        )

        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["suppressed@example.com", "never-suppressed@example.com"],
        }
        removed = await resend.Suppressions.Batch.remove_async(params)
        assert len(removed["data"]) == 1
        assert removed["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"

    async def test_suppressions_batch_remove_async_with_no_matches(self) -> None:
        self.set_mock_json({"data": []})

        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["never-suppressed@example.com"],
        }
        removed = await resend.Suppressions.Batch.remove_async(params)
        assert removed["data"] == []

    async def test_suppressions_batch_remove_async_raises_when_both_provided(
        self,
    ) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
            "ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"],
        }
        with pytest.raises(ValueError):
            _ = await resend.Suppressions.Batch.remove_async(params)

    async def test_suppressions_batch_remove_async_raises_when_neither_provided(
        self,
    ) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {}
        with pytest.raises(ValueError):
            _ = await resend.Suppressions.Batch.remove_async(params)

    async def test_should_batch_remove_suppressions_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
        }
        with pytest.raises(NoContentError):
            _ = await resend.Suppressions.Batch.remove_async(params)


class TestSuppressionsRequestBodyAsync:
    def setup_method(self) -> None:
        resend.api_key = "re_123"
        self.mock_client = AsyncMock()
        self.mock_client.request.return_value = (
            b'{"data": []}',
            200,
            {"content-type": "application/json"},
        )
        self.previous_async_http_client = resend.default_async_http_client
        resend.default_async_http_client = self.mock_client

    def teardown_method(self) -> None:
        resend.default_async_http_client = self.previous_async_http_client

    async def test_batch_remove_async_omits_the_unset_key(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
        }
        await resend.Suppressions.Batch.remove_async(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["url"] == "https://api.resend.com/suppressions/batch/remove"
        assert kwargs["json"] == {"emails": ["one@example.com"]}
        assert "ids" not in kwargs["json"]

    async def test_batch_remove_async_omits_explicit_none_ids(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
            "ids": None,  # type: ignore[typeddict-item]
        }
        await resend.Suppressions.Batch.remove_async(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"] == {"emails": ["one@example.com"]}
        assert "ids" not in kwargs["json"]

    async def test_batch_remove_async_omits_explicit_none_emails(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"],
            "emails": None,  # type: ignore[typeddict-item]
        }
        await resend.Suppressions.Batch.remove_async(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"] == {"ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"]}
        assert "emails" not in kwargs["json"]

    async def test_batch_remove_async_omits_none_from_dynamically_built_params(
        self,
    ) -> None:
        params: Dict[str, Any] = {}
        params["ids"] = None
        params["emails"] = ["one@example.com"]
        await resend.Suppressions.Batch.remove_async(
            cast("resend.Suppressions.Batch.RemoveParams", params)
        )

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"] == {"emails": ["one@example.com"]}
        assert "ids" not in kwargs["json"]

    async def test_batch_remove_async_raises_when_both_keys_are_none(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": None,  # type: ignore[typeddict-item]
            "ids": None,  # type: ignore[typeddict-item]
        }
        with pytest.raises(ValueError):
            await resend.Suppressions.Batch.remove_async(params)
        self.mock_client.request.assert_not_called()
