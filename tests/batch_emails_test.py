from typing import Any, List
from unittest.mock import patch

import resend
from resend import request
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendBatchSend(ResendBaseTest):
    def test_batch_email_send(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {"id": "ae2014de-c168-4c61-8267-70d2662a1ce1"},
                    {"id": "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"},
                ]
            }
        )

        params: List[resend.Batch.SendParams] = [
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hey",
                "html": "<strong>hello, world!</strong>",
            },
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hello",
                "html": "<strong>hello, world!</strong>",
            },
        ]

        emails: resend.Batch.SendResponse = resend.Batch.send(params)
        assert len(emails["data"]) == 2
        assert emails["data"][0]["id"] == "ae2014de-c168-4c61-8267-70d2662a1ce1"
        assert emails["data"][1]["id"] == "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"

    def test_batch_email_send_with_options(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {"id": "ae2014de-c168-4c61-8267-70d2662a1ce1"},
                    {"id": "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"},
                ]
            }
        )

        params: List[resend.Batch.SendParams] = [
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hey",
                "html": "<strong>hello, world!</strong>",
            },
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hello",
                "html": "<strong>hello, world!</strong>",
            },
        ]

        options: resend.Batch.SendOptions = {
            "idempotency_key": "af477dc78aa9fa91fff3b8c0d4a2e1a5",
        }

        emails: resend.Batch.SendResponse = resend.Batch.send(params, options=options)
        assert len(emails["data"]) == 2
        assert emails["data"][0]["id"] == "ae2014de-c168-4c61-8267-70d2662a1ce1"
        assert emails["data"][1]["id"] == "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"

    def test_should_send_batch_email_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        params: List[resend.Batch.SendParams] = [
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hey",
                "html": "<strong>hello, world!</strong>",
            },
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hello",
                "html": "<strong>hello, world!</strong>",
            },
        ]
        with self.assertRaises(NoContentError):
            _ = resend.Batch.send(params)

    def test_batch_email_send_with_strict_validation_mode(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {"id": "ae2014de-c168-4c61-8267-70d2662a1ce1"},
                    {"id": "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"},
                ]
            }
        )

        params: List[resend.Batch.SendParams] = [
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hey",
                "html": "<strong>hello, world!</strong>",
            },
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hello",
                "html": "<strong>hello, world!</strong>",
            },
        ]

        options: resend.Batch.SendOptions = {
            "batch_validation": "strict",
        }

        emails: resend.Batch.SendResponse = resend.Batch.send(params, options=options)
        assert len(emails["data"]) == 2
        assert emails["data"][0]["id"] == "ae2014de-c168-4c61-8267-70d2662a1ce1"
        assert emails["data"][1]["id"] == "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"
        assert "errors" not in emails

    def test_batch_email_send_with_permissive_validation_mode(self) -> None:
        self.set_mock_json(
            {
                "data": [
                    {"id": "ae2014de-c168-4c61-8267-70d2662a1ce1"},
                ],
                "errors": [
                    {
                        "index": 1,
                        "message": "The `to` field is missing.",
                    }
                ],
            }
        )

        params: List[resend.Batch.SendParams] = [
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hey",
                "html": "<strong>hello, world!</strong>",
            },
            {
                "from": "from@resend.dev",
                "to": [],
                "subject": "hello",
                "html": "<strong>hello, world!</strong>",
            },
        ]

        options: resend.Batch.SendOptions = {
            "batch_validation": "permissive",
        }

        emails: resend.Batch.SendResponse = resend.Batch.send(params, options=options)
        assert len(emails["data"]) == 1
        assert emails["data"][0]["id"] == "ae2014de-c168-4c61-8267-70d2662a1ce1"
        assert "errors" in emails
        assert len(emails["errors"]) == 1
        assert emails["errors"][0]["index"] == 1
        assert emails["errors"][0]["message"] == "The `to` field is missing."

    def test_batch_email_send_with_tags(self) -> None:
        self.set_mock_json(
            {
                "data": [{"id": "ae2014de-c168-4c61-8267-70d2662a1ce1"}]
            }
        )

        params: List[resend.Batch.SendParams] = [
            {
                "from": "from@resend.dev",
                "to": ["to@resend.dev"],
                "subject": "hey",
                "html": "<strong>hello, world!</strong>",
                "tags": [{"name": "category", "value": "notification"}],
            }
        ]

        captured_params: List[Any] = []
        original_init = request.Request.__init__

        def capturing_init(instance: Any, *args: Any, **kwargs: Any) -> None:
            captured_params.append(kwargs.get("params"))
            original_init(instance, *args, **kwargs)

        with patch.object(request.Request, "__init__", capturing_init):
            emails: resend.Batch.SendResponse = resend.Batch.send(params)

        assert emails["data"][0]["id"] == "ae2014de-c168-4c61-8267-70d2662a1ce1"

        sent_params = captured_params[0]
        assert sent_params[0]["tags"] == [{"name": "category", "value": "notification"}]
