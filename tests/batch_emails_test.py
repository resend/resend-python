from typing import List
from unittest import TestCase
from unittest.mock import create_autospec

import resend
from resend.exceptions import NoContentError
from resend.http_client import HTTPClient
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

        params: List[resend.Emails.SendParams] = [
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

        params: List[resend.Emails.SendParams] = [
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
        params: List[resend.Emails.SendParams] = [
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

        params: List[resend.Emails.SendParams] = [
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

        params: List[resend.Emails.SendParams] = [
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


class TestBatchRequestBody(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_123"
        self.mock_client = create_autospec(HTTPClient, instance=True)
        self.previous_http_client = resend.default_http_client
        resend.default_http_client = self.mock_client

    def tearDown(self) -> None:
        resend.default_http_client = self.previous_http_client

    def test_batch_send_sends_topic_id(self) -> None:
        self.mock_client.request.return_value = (
            b'{"data": [{"id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"}]}',
            200,
            {"Content-Type": "application/json"},
        )
        params: List[resend.Emails.SendParams] = [
            {
                "from": "from@email.com",
                "to": "to@email.com",
                "subject": "subject",
                "html": "html",
                "topic_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
            }
        ]
        resend.Batch.send(params)

        _, kwargs = self.mock_client.request.call_args
        assert kwargs["json"][0]["topic_id"] == "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
