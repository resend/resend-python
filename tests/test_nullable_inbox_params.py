from resend.inboxes.drafts._inbox_drafts import InboxDrafts
from resend.inboxes.threads.emails._inbox_thread_emails import \
    InboxThreadEmails


def test_optional_inbox_params_accept_none() -> None:
    reply: InboxThreadEmails.ReplyParams = {
        "inbox_id": "inbox_123",
        "thread_id": "thread_123",
        "email_id": "email_123",
        "cc": None,
        "bcc": None,
        "headers": None,
        "attachments": None,
    }
    forward: InboxThreadEmails.ForwardParams = {
        "inbox_id": "inbox_123",
        "thread_id": "thread_123",
        "email_id": "email_123",
        "to": "recipient@example.com",
        "cc": None,
        "bcc": None,
        "headers": None,
        "attachments": None,
    }
    create_draft: InboxDrafts.CreateParams = {
        "inbox_id": "inbox_123",
        "attachments": None,
    }
    send_draft: InboxDrafts.SendParams = {"headers": None}

    assert reply["cc"] is None
    assert forward["bcc"] is None
    assert create_draft["attachments"] is None
    assert send_draft["headers"] is None
