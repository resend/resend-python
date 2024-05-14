import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import resend

# flake8: noqa


class TestResendEmail(unittest.TestCase):
    def test_email_send(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }

        m.json = mock_json
        mock.return_value = m

        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "sender": "from@email.com",
            "subject": "subject",
            "html": "html",
        }
        email: resend.Email = resend.Emails.send(params)
        assert email.id == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
        patcher.stop()

    def test_email_get(self) -> None:
        resend.api_key = "re_123"

        patcher = patch("resend.Request.make_request")
        mock = patcher.start()
        mock.status_code = 200
        m = MagicMock()
        m.status_code = 200

        def mock_json() -> Dict[Any, Any]:
            return {
                "object": "email",
                "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
                "to": ["james@bond.com"],
                "from": "onboarding@resend.dev",
                "created_at": "2023-04-03T22:13:42.674981+00:00",
                "subject": "Hello World",
                "html": "Congrats on sending your <strong>first email</strong>!",
                "text": None,
                "bcc": [None],
                "cc": [None],
                "reply_to": [None],
                "last_event": "delivered",
            }

        m.json = mock_json
        mock.return_value = m

        email: resend.Email = resend.Emails.get(
            email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        )
        assert email.id == "4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
        patcher.stop()
