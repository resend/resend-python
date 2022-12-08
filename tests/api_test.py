import pytest
from klotty import Klotty


def test_invalid_api_key():
    with pytest.raises(ValueError):
        Klotty(api_key="")


def test_invalid_send_email_args():
    with pytest.raises(ValueError):
        client = Klotty(api_key="kl_123")
        client.send_email(
            sender="",
            to="to@email.com",
            text="text",
            subject="subj",
        )

    with pytest.raises(ValueError):
        client = Klotty(api_key="kl_123")
        client.send_email(
            sender="from@email.com",
            to="",
            text="text",
            subject="subj",
        )


def test_missing_subject():
    with pytest.raises(ValueError):
        client = Klotty(api_key="kl_123")
        client.send_email(
            sender="from@email.com",
            to="to@email.com",
            subject="",
            text="text",
        )
