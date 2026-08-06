from typing import Any, Dict, cast
from unittest import TestCase
from unittest.mock import create_autospec

import resend
from resend.exceptions import NoContentError
from resend.http_client import HTTPClient
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestSuppressions(ResendBaseTest):
    def test_suppressions_add(self) -> None:
        self.set_mock_json(
            {
                "object": "suppression",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
            }
        )

        params: resend.Suppressions.AddParams = {"email": "blocked@example.com"}
        added: resend.Suppressions.AddSuppressionResponse = resend.Suppressions.add(
            params
        )
        assert added["object"] == "suppression"
        assert added["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"

    def test_should_add_suppression_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: resend.Suppressions.AddParams = {"email": "blocked@example.com"}
        with self.assertRaises(NoContentError):
            _ = resend.Suppressions.add(params)

    def test_suppressions_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
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

        suppressions: resend.Suppressions.ListResponse = resend.Suppressions.list()
        assert suppressions["object"] == "list"
        assert suppressions["has_more"] is True

        bounced = suppressions["data"][0]
        assert bounced["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert bounced["email"] == "bounced@example.com"
        assert bounced["origin"] == "bounce"
        assert bounced["source_id"] == "479e3145-dd38-476b-932c-529ceb705947"
        assert bounced["created_at"] == "2023-10-06 23:47:56.678+00"

        manual = suppressions["data"][1]
        assert manual["origin"] == "manual"
        assert manual["source_id"] is None

    def test_suppressions_list_entries_have_no_object_field(self) -> None:
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
                    }
                ],
            }
        )

        suppressions = resend.Suppressions.list()
        assert "object" not in suppressions["data"][0]
        assert sorted(suppressions["data"][0].keys()) == [
            "created_at",
            "email",
            "id",
            "origin",
            "source_id",
        ]

    def test_suppressions_list_with_params(self) -> None:
        self.set_mock_json({"object": "list", "has_more": False, "data": []})

        params: resend.Suppressions.ListParams = {
            "origin": "complaint",
            "limit": 25,
            "after": "e169aa45-1ecf-4183-9955-b1499d5701d3",
        }
        suppressions = resend.Suppressions.list(params)
        assert suppressions["has_more"] is False
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/suppressions?origin=complaint&limit=25&after=e169aa45-1ecf-4183-9955-b1499d5701d3"
        )

    def test_should_list_suppressions_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Suppressions.list()

    def test_suppressions_get(self) -> None:
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

        suppression: resend.Suppression = resend.Suppressions.get(
            "e169aa45-1ecf-4183-9955-b1499d5701d3"
        )
        assert suppression["object"] == "suppression"
        assert suppression["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert suppression["email"] == "bounced@example.com"
        assert suppression["origin"] == "bounce"
        assert suppression["source_id"] == "479e3145-dd38-476b-932c-529ceb705947"

    def test_suppressions_get_with_null_source_id(self) -> None:
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

        suppression = resend.Suppressions.get("manual@example.com")
        assert suppression["origin"] == "manual"
        assert suppression["source_id"] is None

    def test_suppressions_get_encodes_email_identifier(self) -> None:
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

        suppression = resend.Suppressions.get("user+tag@example.com")
        assert suppression["email"] == "user+tag@example.com"
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/suppressions/user%2Btag%40example.com"
        )

    def test_suppressions_get_raises_without_identifier(self) -> None:
        with self.assertRaises(ValueError):
            _ = resend.Suppressions.get("")

    def test_should_get_suppression_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Suppressions.get("e169aa45-1ecf-4183-9955-b1499d5701d3")

    def test_suppressions_remove(self) -> None:
        self.set_mock_json(
            {
                "object": "suppression",
                "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
                "deleted": True,
            }
        )

        removed: resend.Suppressions.RemoveSuppressionResponse = (
            resend.Suppressions.remove("blocked@example.com")
        )
        assert removed["object"] == "suppression"
        assert removed["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert removed["deleted"] is True
        assert (
            self.mock.call_args.kwargs["url"]
            == "https://api.resend.com/suppressions/blocked%40example.com"
        )

    def test_suppressions_remove_raises_without_identifier(self) -> None:
        with self.assertRaises(ValueError):
            _ = resend.Suppressions.remove("")

    def test_should_remove_suppression_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Suppressions.remove("blocked@example.com")

    def test_suppressions_batch_add(self) -> None:
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
        added: resend.Suppressions.Batch.AddResponse = resend.Suppressions.Batch.add(
            params
        )
        assert len(added["data"]) == 2
        assert added["data"][0]["object"] == "suppression"
        assert added["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert added["data"][1]["id"] == "fd61172c-cafc-40f5-b049-b45947779a29"

    def test_suppressions_batch_add_dedupes_server_side(self) -> None:
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
            "emails": [
                "ONE@example.com",
                "one@example.com",
                " one@example.com ",
            ],
        }
        added = resend.Suppressions.Batch.add(params)
        assert len(added["data"]) == 1
        assert added["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"

    def test_should_batch_add_suppressions_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Suppressions.Batch.AddParams = {"emails": ["one@example.com"]}
        with self.assertRaises(NoContentError):
            _ = resend.Suppressions.Batch.add(params)

    def test_suppressions_batch_remove_with_emails(self) -> None:
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
        removed: resend.Suppressions.Batch.RemoveResponse = (
            resend.Suppressions.Batch.remove(params)
        )
        assert removed["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"
        assert removed["data"][0]["deleted"] is True

    def test_suppressions_batch_remove_with_ids(self) -> None:
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
        removed = resend.Suppressions.Batch.remove(params)
        assert len(removed["data"]) == 2
        assert removed["data"][0]["deleted"] is True
        assert removed["data"][1]["deleted"] is True

    def test_suppressions_batch_remove_omits_identifiers_that_were_not_suppressed(
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
        removed = resend.Suppressions.Batch.remove(params)
        assert len(removed["data"]) == 1
        assert removed["data"][0]["id"] == "e169aa45-1ecf-4183-9955-b1499d5701d3"

    def test_suppressions_batch_remove_with_no_matches(self) -> None:
        self.set_mock_json({"data": []})

        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["never-suppressed@example.com"],
        }
        removed = resend.Suppressions.Batch.remove(params)
        assert removed["data"] == []

    def test_suppressions_batch_remove_raises_when_both_provided(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
            "ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"],
        }
        with self.assertRaises(ValueError):
            _ = resend.Suppressions.Batch.remove(params)

    def test_suppressions_batch_remove_raises_when_neither_provided(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {}
        with self.assertRaises(ValueError):
            _ = resend.Suppressions.Batch.remove(params)

    def test_should_batch_remove_suppressions_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
        }
        with self.assertRaises(NoContentError):
            _ = resend.Suppressions.Batch.remove(params)


class TestSuppressionsRequestBody(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_123"
        self.mock_client = create_autospec(HTTPClient, instance=True)
        self.mock_client.name = "mock"
        self.mock_client.request.return_value = (
            b'{"data": []}',
            200,
            {"Content-Type": "application/json"},
        )
        self.previous_http_client = resend.default_http_client
        resend.default_http_client = self.mock_client

    def tearDown(self) -> None:
        resend.default_http_client = self.previous_http_client

    def test_batch_remove_omits_the_unset_key(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
        }
        resend.Suppressions.Batch.remove(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["url"] == "https://api.resend.com/suppressions/batch/remove"
        assert kwargs["json"] == {"emails": ["one@example.com"]}
        assert "ids" not in kwargs["json"]

    def test_batch_remove_with_ids_omits_emails(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"],
        }
        resend.Suppressions.Batch.remove(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"] == {"ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"]}
        assert "emails" not in kwargs["json"]

    def test_batch_remove_omits_explicit_none_ids(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": ["one@example.com"],
            "ids": None,  # type: ignore[typeddict-item]
        }
        resend.Suppressions.Batch.remove(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"] == {"emails": ["one@example.com"]}
        assert "ids" not in kwargs["json"]

    def test_batch_remove_omits_explicit_none_emails(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"],
            "emails": None,  # type: ignore[typeddict-item]
        }
        resend.Suppressions.Batch.remove(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"] == {"ids": ["e169aa45-1ecf-4183-9955-b1499d5701d3"]}
        assert "emails" not in kwargs["json"]

    def test_batch_remove_omits_none_from_dynamically_built_params(self) -> None:
        params: Dict[str, Any] = {}
        params["ids"] = None
        params["emails"] = ["one@example.com"]
        resend.Suppressions.Batch.remove(
            cast("resend.Suppressions.Batch.RemoveParams", params)
        )

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"] == {"emails": ["one@example.com"]}
        assert "ids" not in kwargs["json"]

    def test_batch_remove_raises_when_both_keys_are_none(self) -> None:
        params: resend.Suppressions.Batch.RemoveParams = {
            "emails": None,  # type: ignore[typeddict-item]
            "ids": None,  # type: ignore[typeddict-item]
        }
        with self.assertRaises(ValueError):
            resend.Suppressions.Batch.remove(params)
        self.mock_client.request.assert_not_called()
