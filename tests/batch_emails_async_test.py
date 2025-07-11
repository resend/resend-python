from typing import List

import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendBatchSendAsync(ResendBaseTest):
    async def test_batch_email_send_async(self) -> None:
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

        emails: resend.Batch.SendResponse = await resend.Batch.send_async(params)
        assert len(emails["data"]) == 2
        assert emails["data"][0]["id"] == "ae2014de-c168-4c61-8267-70d2662a1ce1"
        assert emails["data"][1]["id"] == "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"

    async def test_batch_email_send_async_with_options(self) -> None:
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

        emails: resend.Batch.SendResponse = await resend.Batch.send_async(
            params, options=options
        )
        assert len(emails["data"]) == 2
        assert emails["data"][0]["id"] == "ae2014de-c168-4c61-8267-70d2662a1ce1"
        assert emails["data"][1]["id"] == "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"

    async def test_should_send_batch_email_async_raise_exception_when_no_content(
        self,
    ) -> None:
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
            _ = await resend.Batch.send_async(params)
