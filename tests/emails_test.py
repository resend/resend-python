import resend
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendEmail(ResendBaseTest):

    def test_email_send_with_from(self) -> None:
        self.set_mock_json(
            {
                "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
            }
        )

        params: resend.Emails.SendParams = {
            "to": "to@email.com",
            "from": "from@email.com",
            "subject": "subject",
            "html": "html",
        }
        email: resend.Email = resend.Emails.send(params)
        assert email["id"] == "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"

    def test_email_get(self) -> None:
        self.set_mock_json(
            {
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
        )

        email: resend.Email = resend.Emails.get(
            email_id="4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        )
        assert email["id"] == "4ef9a417-02e9-4d39-ad75-9611e0fcc33c"
