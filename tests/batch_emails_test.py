import unittest
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class TestResendBatchSend(unittest.TestCase):
    def test_batch_email_send(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "data": [
                    {"id": "ae2014de-c168-4c61-8267-70d2662a1ce1"},
                    {"id": "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"},
                ]
            }

        m.json = mock_json
        mock.return_value = m

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
        emails: List[resend.Email] = resend.Batch.send(params)
        assert len(emails) == 2
        assert emails[0].id == "ae2014de-c168-4c61-8267-70d2662a1ce1"
        assert emails[1].id == "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"
        patcher.stop()
