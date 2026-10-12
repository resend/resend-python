from typing import Any, Dict
from unittest import TestCase
from unittest.mock import create_autospec

import resend
from resend import HTTPClient
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa

INBOX_ID = "b3e2b2b6-3f0e-4c8e-9ad3-2f43a1e2c7f1"
LABEL_ID = "7f9c1d2e-4a6b-4c3d-8e15-9b0a7c6d5e34"
THREAD_ID = "4d8e2a1c-9b3f-4c6d-8a21-3e5f7c9c0d12"
EMAIL_ID = "5b1a9f47-2c8d-4e6f-9a03-1d2e3f4a5b60"
DRAFT_ID = "c3a1e8b4-2d5f-4a7c-9e10-6b8d7f5a4c32"
SENT_EMAIL_ID = "6a0c8e58-3d9e-4f7a-8b14-2e3f4a5b6c71"

INBOX: Dict[str, Any] = {
    "object": "inbox",
    "id": INBOX_ID,
    "name": "Customer Support",
    "email_address": "support@acme.com",
    "domain_id": "d91cd9bd-1176-453e-8fc1-35364d380206",
    "receiving_address": None,
    "from_name": "Ada from Support",
    "unread": 3,
    "drafts": 2,
    "last_received": "2026-08-05T14:03:11.229Z",
    "created_at": "2026-08-01T09:12:44.512Z",
}

THREAD_LABEL: Dict[str, Any] = {"id": LABEL_ID, "name": "Urgent", "color": "#E93D82"}

THREAD: Dict[str, Any] = {
    "id": THREAD_ID,
    "subject": "Refund for order 1041",
    "from": "ada@example.org",
    "to": ["support@acme.com"],
    "cc": [],
    "bcc": [],
    "labels": [THREAD_LABEL],
    "message_count": 2,
    "has_attachment": True,
    "has_draft": False,
    "read": False,
    "received_at": "2026-08-05T14:03:11.229Z",
    "folder": "inbox",
}

THREAD_SUMMARY: Dict[str, Any] = {
    "object": "inbox_thread",
    "id": THREAD_ID,
    "subject": "Refund for order 1041",
    "folder": "inbox",
    "labels": [THREAD_LABEL],
    "read": False,
}

THREAD_EMAIL: Dict[str, Any] = {
    "id": EMAIL_ID,
    "direction": "inbound",
    "from": "Ada Lovelace <ada@example.org>",
    "to": ["support@acme.com"],
    "cc": [],
    "bcc": [],
    "reply_to": ["replies@example.org"],
    "subject": "Refund for order 1041",
    "message_id": "<1041@example.org>",
    "html": "<p>Could I get a refund for order 1041?</p>",
    "text": "Could I get a refund for order 1041?",
    "attachments": [
        {
            "id": "9d4f2b81-6c3a-4e7d-8b12-0a5c6d7e8f90",
            "filename": "receipt.pdf",
            "size": 20841,
        }
    ],
    "read": False,
    "received_at": "2026-08-05T14:03:11.229Z",
}

DRAFT: Dict[str, Any] = {
    "object": "inbox_draft",
    "id": DRAFT_ID,
    "type": "standalone",
    "to": ["ada@example.org"],
    "cc": [],
    "bcc": [],
    "subject": "Refund for order 1041",
    "html": "<p>Refund issued for order 1041.</p>",
    "text": "Refund issued for order 1041.",
    "thread_id": None,
    "reply_to_email_id": None,
    "email_id": None,
    "created_at": "2026-08-05T14:12:04.110Z",
    "updated_at": "2026-08-05T14:12:04.110Z",
}


class TestResendInboxes(ResendBaseTest):
    def test_inboxes_create(self) -> None:
        self.set_mock_json({"object": "inbox", "id": INBOX_ID})
        params: resend.Inboxes.CreateParams = {
            "email_address": "support@acme.com",
            "name": "Customer Support",
            "from_name": "Ada from Support",
            "forwarding": False,
        }
        inbox: resend.Inboxes.CreateResponse = resend.Inboxes.create(params)
        assert inbox["object"] == "inbox"
        assert inbox["id"] == INBOX_ID

    def test_should_create_inboxes_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.create({"email_address": "support@acme.com"})

    def test_inboxes_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": INBOX_ID,
                        "name": "Customer Support",
                        "email_address": "support@acme.com",
                        "from_name": None,
                        "unread": 3,
                        "last_received": None,
                    }
                ],
            }
        )
        inboxes: resend.Inboxes.ListResponse = resend.Inboxes.list({"limit": 10})
        assert inboxes["object"] == "list"
        assert inboxes["has_more"] is False
        assert inboxes["data"][0]["id"] == INBOX_ID
        assert inboxes["data"][0]["email_address"] == "support@acme.com"
        assert inboxes["data"][0]["from_name"] is None

    def test_should_list_inboxes_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.list()

    def test_inboxes_get(self) -> None:
        self.set_mock_json(INBOX)
        inbox: resend.Inbox = resend.Inboxes.get(INBOX_ID)
        assert inbox["object"] == "inbox"
        assert inbox["id"] == INBOX_ID
        assert inbox["receiving_address"] is None
        assert inbox["unread"] == 3
        assert inbox["drafts"] == 2

    def test_should_get_inboxes_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.get(INBOX_ID)

    def test_inboxes_update(self) -> None:
        self.set_mock_json({"object": "inbox", "id": INBOX_ID})
        params: resend.Inboxes.UpdateParams = {"id": INBOX_ID, "name": "Support"}
        inbox: resend.Inboxes.UpdateResponse = resend.Inboxes.update(params)
        assert inbox["object"] == "inbox"
        assert inbox["id"] == INBOX_ID

    def test_should_update_inboxes_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.update({"id": INBOX_ID, "name": "Support"})

    def test_inboxes_remove(self) -> None:
        self.set_mock_json({"object": "inbox", "id": INBOX_ID, "deleted": True})
        removed: resend.Inboxes.RemoveResponse = resend.Inboxes.remove(INBOX_ID)
        assert removed["id"] == INBOX_ID
        assert removed["deleted"] is True

    def test_should_remove_inboxes_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.remove(INBOX_ID)


class TestResendInboxAgent(ResendBaseTest):
    def test_inbox_agent_get(self) -> None:
        self.set_mock_json(
            {
                "object": "inbox_agent",
                "instructions": None,
                "tone": None,
                "enabled_actions": [],
            }
        )
        agent: resend.InboxAgentSettings = resend.Inboxes.Agent.get(INBOX_ID)
        assert agent["object"] == "inbox_agent"
        assert agent["instructions"] is None
        assert agent["enabled_actions"] == []

    def test_should_get_inbox_agent_raise_exception_when_no_content(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Agent.get(INBOX_ID)

    def test_inbox_agent_update(self) -> None:
        self.set_mock_json(
            {"object": "inbox_agent", "id": "a1f84a4e-6f2b-4f0a-9c1d-8a2e5b3c7d90"}
        )
        params: resend.Inboxes.Agent.UpdateParams = {
            "inbox_id": INBOX_ID,
            "tone": "friendly and concise",
            "enabled_actions": ["draft_reply", "add_labels"],
        }
        agent: resend.Inboxes.Agent.UpdateResponse = resend.Inboxes.Agent.update(
            params
        )
        assert agent["object"] == "inbox_agent"
        assert agent["id"] == "a1f84a4e-6f2b-4f0a-9c1d-8a2e5b3c7d90"

    def test_should_update_inbox_agent_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Agent.update({"inbox_id": INBOX_ID, "tone": None})


class TestResendInboxLabels(ResendBaseTest):
    def test_inbox_labels_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "data": [
                    {
                        "id": LABEL_ID,
                        "name": "Urgent",
                        "color": "#E93D82",
                        "created_at": "2026-08-05T14:07:42.881Z",
                    }
                ],
            }
        )
        labels: resend.Inboxes.Labels.ListResponse = resend.Inboxes.Labels.list(
            INBOX_ID
        )
        assert labels["object"] == "list"
        assert labels["data"][0]["id"] == LABEL_ID
        assert labels["data"][0]["color"] == "#E93D82"

    def test_should_list_inbox_labels_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Labels.list(INBOX_ID)

    def test_inbox_labels_create(self) -> None:
        self.set_mock_json({"object": "inbox_label", "id": LABEL_ID})
        params: resend.Inboxes.Labels.CreateParams = {
            "inbox_id": INBOX_ID,
            "name": "Urgent",
            "color": "#E93D82",
        }
        label: resend.Inboxes.Labels.CreateResponse = resend.Inboxes.Labels.create(
            params
        )
        assert label["object"] == "inbox_label"
        assert label["id"] == LABEL_ID

    def test_should_create_inbox_labels_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Labels.create({"inbox_id": INBOX_ID, "name": "Urgent"})

    def test_inbox_labels_update(self) -> None:
        self.set_mock_json({"object": "inbox_label", "id": LABEL_ID})
        params: resend.Inboxes.Labels.UpdateParams = {
            "inbox_id": INBOX_ID,
            "id": LABEL_ID,
            "name": "Billing",
            "color": "#F76B15",
        }
        label: resend.Inboxes.Labels.UpdateResponse = resend.Inboxes.Labels.update(
            params
        )
        assert label["object"] == "inbox_label"
        assert label["id"] == LABEL_ID

    def test_should_update_inbox_labels_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Labels.update(
                {"inbox_id": INBOX_ID, "id": LABEL_ID, "name": "Billing"}
            )

    def test_inbox_labels_remove(self) -> None:
        self.set_mock_json({"object": "inbox_label", "id": LABEL_ID, "deleted": True})
        removed: resend.Inboxes.Labels.RemoveResponse = resend.Inboxes.Labels.remove(
            INBOX_ID, LABEL_ID
        )
        assert removed["id"] == LABEL_ID
        assert removed["deleted"] is True

    def test_should_remove_inbox_labels_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Labels.remove(INBOX_ID, LABEL_ID)


class TestResendInboxThreads(ResendBaseTest):
    def test_inbox_threads_list(self) -> None:
        self.set_mock_json({"object": "list", "has_more": True, "data": [THREAD]})
        params: resend.Inboxes.Threads.ListParams = {
            "folders": ["inbox", "sent"],
            "read": False,
            "limit": 10,
        }
        threads: resend.Inboxes.Threads.ListResponse = resend.Inboxes.Threads.list(
            INBOX_ID, params
        )
        assert threads["object"] == "list"
        assert threads["has_more"] is True
        thread = threads["data"][0]
        assert thread["id"] == THREAD_ID
        assert thread["from"] == "ada@example.org"
        assert thread["labels"][0]["color"] == "#E93D82"
        assert thread["folder"] == "inbox"

    def test_should_list_inbox_threads_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.list(INBOX_ID)

    def test_inbox_threads_search(self) -> None:
        result = dict(THREAD)
        result["matched_email_id"] = "e8a3f1c6-2b9d-4e5a-a7c4-9d1b6f3e2a80"
        result["highlights"] = {"subject": ["September **invoice**"]}
        self.set_mock_json({"object": "list", "has_more": False, "data": [result]})
        params: resend.Inboxes.Threads.SearchParams = {
            "query": "invoice -draft",
            "has_attachment": True,
        }
        threads: resend.Inboxes.Threads.SearchResponse = (
            resend.Inboxes.Threads.search(INBOX_ID, params)
        )
        assert threads["object"] == "list"
        match = threads["data"][0]
        assert match["matched_email_id"] == "e8a3f1c6-2b9d-4e5a-a7c4-9d1b6f3e2a80"
        assert match["highlights"]["subject"] == ["September **invoice**"]

    def test_should_search_inbox_threads_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.search(INBOX_ID)

    def test_inbox_threads_get(self) -> None:
        self.set_mock_json(THREAD_SUMMARY)
        thread: resend.InboxThreadSummary = resend.Inboxes.Threads.get(
            INBOX_ID, THREAD_ID
        )
        assert thread["object"] == "inbox_thread"
        assert thread["id"] == THREAD_ID
        assert thread["read"] is False

    def test_should_get_inbox_threads_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.get(INBOX_ID, THREAD_ID)

    def test_inbox_threads_update(self) -> None:
        summary = dict(THREAD_SUMMARY)
        summary["folder"] = "archive"
        summary["read"] = True
        self.set_mock_json(summary)
        params: resend.Inboxes.Threads.UpdateParams = {
            "inbox_id": INBOX_ID,
            "id": THREAD_ID,
            "read": True,
            "folder": "archive",
            "add_label_ids": [LABEL_ID],
        }
        thread: resend.InboxThreadSummary = resend.Inboxes.Threads.update(params)
        assert thread["folder"] == "archive"
        assert thread["read"] is True

    def test_should_update_inbox_threads_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.update(
                {"inbox_id": INBOX_ID, "id": THREAD_ID, "read": True}
            )

    def test_inbox_threads_remove(self) -> None:
        self.set_mock_json({"object": "inbox_thread", "id": THREAD_ID, "deleted": True})
        removed: resend.Inboxes.Threads.RemoveResponse = (
            resend.Inboxes.Threads.remove(INBOX_ID, THREAD_ID)
        )
        assert removed["id"] == THREAD_ID
        assert removed["deleted"] is True

    def test_should_remove_inbox_threads_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.remove(INBOX_ID, THREAD_ID)


class TestResendInboxThreadEmails(ResendBaseTest):
    def test_inbox_thread_emails_list(self) -> None:
        self.set_mock_json({"object": "list", "has_more": False, "data": [THREAD_EMAIL]})
        emails: resend.Inboxes.Threads.Emails.ListResponse = (
            resend.Inboxes.Threads.Emails.list(INBOX_ID, THREAD_ID, {"limit": 5})
        )
        assert emails["object"] == "list"
        email = emails["data"][0]
        assert email["id"] == EMAIL_ID
        assert email["from"] == "Ada Lovelace <ada@example.org>"
        assert email["attachments"][0]["filename"] == "receipt.pdf"

    def test_should_list_inbox_thread_emails_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.Emails.list(INBOX_ID, THREAD_ID)

    def test_inbox_thread_emails_get(self) -> None:
        self.set_mock_json(THREAD_EMAIL)
        email: resend.InboxThreadEmail = resend.Inboxes.Threads.Emails.get(
            INBOX_ID, THREAD_ID, EMAIL_ID
        )
        assert email["id"] == EMAIL_ID
        assert email["direction"] == "inbound"
        assert email["reply_to"] == ["replies@example.org"]

    def test_should_get_inbox_thread_emails_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.Emails.get(INBOX_ID, THREAD_ID, EMAIL_ID)

    def test_inbox_thread_emails_reply(self) -> None:
        self.set_mock_json({"id": SENT_EMAIL_ID})
        params: resend.Inboxes.Threads.Emails.ReplyParams = {
            "inbox_id": INBOX_ID,
            "thread_id": THREAD_ID,
            "email_id": EMAIL_ID,
            "text": "Refund issued for order 1041.",
            "reply_all": True,
            "attachments": [{"filename": "note.txt", "content": "aGVsbG8="}],
        }
        reply: resend.Inboxes.Threads.Emails.ReplyResponse = (
            resend.Inboxes.Threads.Emails.reply(params)
        )
        assert reply["id"] == SENT_EMAIL_ID

    def test_should_reply_inbox_thread_emails_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.Emails.reply(
                {
                    "inbox_id": INBOX_ID,
                    "thread_id": THREAD_ID,
                    "email_id": EMAIL_ID,
                    "text": "Hi",
                }
            )

    def test_inbox_thread_emails_forward(self) -> None:
        self.set_mock_json({"id": SENT_EMAIL_ID})
        params: resend.Inboxes.Threads.Emails.ForwardParams = {
            "inbox_id": INBOX_ID,
            "thread_id": THREAD_ID,
            "email_id": EMAIL_ID,
            "to": ["colleague@example.org"],
            "text": "Flagging this refund request for you.",
        }
        forward: resend.Inboxes.Threads.Emails.ForwardResponse = (
            resend.Inboxes.Threads.Emails.forward(params)
        )
        assert forward["id"] == SENT_EMAIL_ID

    def test_should_forward_inbox_thread_emails_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Threads.Emails.forward(
                {
                    "inbox_id": INBOX_ID,
                    "thread_id": THREAD_ID,
                    "email_id": EMAIL_ID,
                    "to": "colleague@example.org",
                }
            )


class TestResendInboxDrafts(ResendBaseTest):
    def test_inbox_drafts_list(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": DRAFT_ID,
                        "type": "standalone",
                        "to": ["ada@example.org"],
                        "cc": [],
                        "bcc": [],
                        "subject": "Refund for order 1041",
                        "snippet": "Refund issued for order 1041.",
                        "thread_id": None,
                        "reply_to_email_id": None,
                        "updated_at": "2026-08-05T14:12:04.110Z",
                    }
                ],
            }
        )
        drafts: resend.Inboxes.Drafts.ListResponse = resend.Inboxes.Drafts.list(
            INBOX_ID
        )
        assert drafts["object"] == "list"
        assert drafts["data"][0]["id"] == DRAFT_ID
        assert drafts["data"][0]["snippet"] == "Refund issued for order 1041."

    def test_should_list_inbox_drafts_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Drafts.list(INBOX_ID)

    def test_inbox_drafts_create(self) -> None:
        self.set_mock_json({"object": "inbox_draft", "id": DRAFT_ID})
        params: resend.Inboxes.Drafts.CreateParams = {
            "inbox_id": INBOX_ID,
            "to": ["ada@example.org"],
            "subject": "Refund for order 1041",
            "text": "Refund issued for order 1041.",
        }
        draft: resend.Inboxes.Drafts.CreateResponse = resend.Inboxes.Drafts.create(
            params
        )
        assert draft["object"] == "inbox_draft"
        assert draft["id"] == DRAFT_ID

    def test_should_create_inbox_drafts_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Drafts.create({"inbox_id": INBOX_ID, "text": "Hi"})

    def test_inbox_drafts_get(self) -> None:
        self.set_mock_json(DRAFT)
        draft: resend.InboxDraft = resend.Inboxes.Drafts.get(INBOX_ID, DRAFT_ID)
        assert draft["object"] == "inbox_draft"
        assert draft["id"] == DRAFT_ID
        assert draft["type"] == "standalone"
        assert draft["email_id"] is None

    def test_should_get_inbox_drafts_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Drafts.get(INBOX_ID, DRAFT_ID)

    def test_inbox_drafts_update(self) -> None:
        draft_json = dict(DRAFT)
        draft_json["html"] = None
        self.set_mock_json(draft_json)
        params: resend.Inboxes.Drafts.UpdateParams = {
            "inbox_id": INBOX_ID,
            "id": DRAFT_ID,
            "text": "Refund issued for order 1041.",
            "cc": None,
        }
        draft: resend.InboxDraft = resend.Inboxes.Drafts.update(params)
        assert draft["id"] == DRAFT_ID
        assert draft["html"] is None

    def test_should_update_inbox_drafts_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Drafts.update(
                {"inbox_id": INBOX_ID, "id": DRAFT_ID, "subject": None}
            )

    def test_inbox_drafts_remove(self) -> None:
        self.set_mock_json({"object": "inbox_draft", "id": DRAFT_ID, "deleted": True})
        removed: resend.Inboxes.Drafts.RemoveResponse = resend.Inboxes.Drafts.remove(
            INBOX_ID, DRAFT_ID
        )
        assert removed["id"] == DRAFT_ID
        assert removed["deleted"] is True

    def test_should_remove_inbox_drafts_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Drafts.remove(INBOX_ID, DRAFT_ID)

    def test_inbox_drafts_send(self) -> None:
        self.set_mock_json({"id": SENT_EMAIL_ID})
        sent: resend.Inboxes.Drafts.SendResponse = resend.Inboxes.Drafts.send(
            INBOX_ID, DRAFT_ID
        )
        assert sent["id"] == SENT_EMAIL_ID

    def test_should_send_inbox_drafts_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.Inboxes.Drafts.send(INBOX_ID, DRAFT_ID)


class TestInboxesRequest(TestCase):
    def setUp(self) -> None:
        resend.api_key = "re_123"
        self.mock_client = create_autospec(HTTPClient, instance=True)
        self.mock_client.name = "mock"
        self.mock_client.request.return_value = (
            b'{"object": "inbox", "id": "b3e2b2b6-3f0e-4c8e-9ad3-2f43a1e2c7f1"}',
            200,
            {"Content-Type": "application/json"},
        )
        self.previous_http_client = resend.default_http_client
        resend.default_http_client = self.mock_client

    def tearDown(self) -> None:
        resend.default_http_client = self.previous_http_client

    def last_request(self) -> Dict[str, Any]:
        _, kwargs = self.mock_client.request.call_args
        return dict(kwargs)

    def test_create_posts_the_params(self) -> None:
        resend.Inboxes.create({"email_address": "support@acme.com", "forwarding": True})
        req = self.last_request()
        assert req["method"] == "post"
        assert req["url"] == "https://api.resend.com/inboxes"
        assert req["json"] == {"email_address": "support@acme.com", "forwarding": True}

    def test_list_adds_the_pagination_query(self) -> None:
        resend.Inboxes.list({"limit": 2, "after": INBOX_ID})
        req = self.last_request()
        assert req["method"] == "get"
        assert req["url"] == f"https://api.resend.com/inboxes?limit=2&after={INBOX_ID}"

    def test_get_encodes_an_email_address(self) -> None:
        resend.Inboxes.get("support@acme.com")
        assert (
            self.last_request()["url"]
            == "https://api.resend.com/inboxes/support%40acme.com"
        )

    def test_update_keeps_the_id_out_of_the_body(self) -> None:
        resend.Inboxes.update({"id": INBOX_ID, "from_name": ""})
        req = self.last_request()
        assert req["method"] == "patch"
        assert req["url"] == f"https://api.resend.com/inboxes/{INBOX_ID}"
        assert req["json"] == {"from_name": ""}

    def test_remove_deletes_the_inbox(self) -> None:
        resend.Inboxes.remove(INBOX_ID)
        req = self.last_request()
        assert req["method"] == "delete"
        assert req["url"] == f"https://api.resend.com/inboxes/{INBOX_ID}"

    def test_agent_get_and_update(self) -> None:
        resend.Inboxes.Agent.get(INBOX_ID)
        assert self.last_request()["url"] == f"https://api.resend.com/inboxes/{INBOX_ID}/agent"

        resend.Inboxes.Agent.update(
            {"inbox_id": INBOX_ID, "instructions": None, "enabled_actions": []}
        )
        req = self.last_request()
        assert req["method"] == "patch"
        assert req["url"] == f"https://api.resend.com/inboxes/{INBOX_ID}/agent"
        assert req["json"] == {"instructions": None, "enabled_actions": []}

    def test_labels_paths_and_bodies(self) -> None:
        base = f"https://api.resend.com/inboxes/{INBOX_ID}/labels"
        resend.Inboxes.Labels.list(INBOX_ID)
        assert self.last_request()["url"] == base

        resend.Inboxes.Labels.create({"inbox_id": INBOX_ID, "name": "Urgent"})
        req = self.last_request()
        assert (req["method"], req["url"], req["json"]) == (
            "post",
            base,
            {"name": "Urgent"},
        )

        resend.Inboxes.Labels.update(
            {"inbox_id": INBOX_ID, "id": LABEL_ID, "color": "#F76B15"}
        )
        req = self.last_request()
        assert (req["method"], req["url"], req["json"]) == (
            "patch",
            f"{base}/{LABEL_ID}",
            {"color": "#F76B15"},
        )

        resend.Inboxes.Labels.remove(INBOX_ID, LABEL_ID)
        req = self.last_request()
        assert (req["method"], req["url"]) == ("delete", f"{base}/{LABEL_ID}")

    def test_threads_list_joins_lists_and_lowercases_booleans(self) -> None:
        resend.Inboxes.Threads.list(
            INBOX_ID,
            {"folders": ["inbox", "sent"], "labels": [LABEL_ID], "read": False},
        )
        assert self.last_request()["url"] == (
            f"https://api.resend.com/inboxes/{INBOX_ID}/threads"
            f"?folders=inbox%2Csent&labels={LABEL_ID}&read=false"
        )

    def test_threads_search_builds_the_query(self) -> None:
        params: resend.Inboxes.Threads.SearchParams = {
            "query": "invoice -draft",
            "from": ["isabella@example.com", "carolina@example.com"],
            "has_attachment": True,
            "start_date": "2026-09-01",
        }
        resend.Inboxes.Threads.search(INBOX_ID, params)
        assert self.last_request()["url"] == (
            f"https://api.resend.com/inboxes/{INBOX_ID}/threads/search"
            "?query=invoice+-draft"
            "&from=isabella%40example.com%2Ccarolina%40example.com"
            "&has_attachment=true&start_date=2026-09-01"
        )

    def test_threads_get_update_and_remove(self) -> None:
        url = f"https://api.resend.com/inboxes/{INBOX_ID}/threads/{THREAD_ID}"
        resend.Inboxes.Threads.get(INBOX_ID, THREAD_ID)
        assert self.last_request()["url"] == url

        resend.Inboxes.Threads.update(
            {
                "inbox_id": INBOX_ID,
                "id": THREAD_ID,
                "folder": "archive",
                "add_label_ids": [LABEL_ID],
                "remove_label_ids": ["2b6d0f4e-8a1c-4e3b-9d57-1c0e8a6f4b21"],
            }
        )
        req = self.last_request()
        assert (req["method"], req["url"]) == ("patch", url)
        assert req["json"] == {
            "folder": "archive",
            "add_label_ids": [LABEL_ID],
            "remove_label_ids": ["2b6d0f4e-8a1c-4e3b-9d57-1c0e8a6f4b21"],
        }

        resend.Inboxes.Threads.remove(INBOX_ID, THREAD_ID)
        req = self.last_request()
        assert (req["method"], req["url"]) == ("delete", url)

    def test_thread_emails_paths_and_bodies(self) -> None:
        base = f"https://api.resend.com/inboxes/{INBOX_ID}/threads/{THREAD_ID}/emails"
        resend.Inboxes.Threads.Emails.list(INBOX_ID, THREAD_ID, {"before": EMAIL_ID})
        assert self.last_request()["url"] == f"{base}?before={EMAIL_ID}"

        resend.Inboxes.Threads.Emails.get(INBOX_ID, THREAD_ID, EMAIL_ID)
        assert self.last_request()["url"] == f"{base}/{EMAIL_ID}"

        attachment: resend.Attachment = {"filename": "note.txt", "content": "aGVsbG8="}
        resend.Inboxes.Threads.Emails.reply(
            {
                "inbox_id": INBOX_ID,
                "thread_id": THREAD_ID,
                "email_id": EMAIL_ID,
                "html": "<p>Done.</p>",
                "reply_all": True,
                "attachments": [attachment],
            }
        )
        req = self.last_request()
        assert (req["method"], req["url"]) == ("post", f"{base}/{EMAIL_ID}/reply")
        assert req["json"] == {
            "html": "<p>Done.</p>",
            "reply_all": True,
            "attachments": [attachment],
        }

        resend.Inboxes.Threads.Emails.forward(
            {
                "inbox_id": INBOX_ID,
                "thread_id": THREAD_ID,
                "email_id": EMAIL_ID,
                "to": "colleague@example.org",
            }
        )
        req = self.last_request()
        assert (req["method"], req["url"]) == ("post", f"{base}/{EMAIL_ID}/forward")
        assert req["json"] == {"to": "colleague@example.org"}

    def test_drafts_paths_and_bodies(self) -> None:
        base = f"https://api.resend.com/inboxes/{INBOX_ID}/drafts"
        resend.Inboxes.Drafts.list(INBOX_ID, {"limit": 1})
        assert self.last_request()["url"] == f"{base}?limit=1"

        resend.Inboxes.Drafts.create(
            {
                "inbox_id": INBOX_ID,
                "thread_id": THREAD_ID,
                "reply_to_email_id": EMAIL_ID,
                "to": [],
            }
        )
        req = self.last_request()
        assert (req["method"], req["url"]) == ("post", base)
        assert req["json"] == {
            "thread_id": THREAD_ID,
            "reply_to_email_id": EMAIL_ID,
            "to": [],
        }

        resend.Inboxes.Drafts.get(INBOX_ID, DRAFT_ID)
        assert self.last_request()["url"] == f"{base}/{DRAFT_ID}"

        resend.Inboxes.Drafts.update({"inbox_id": INBOX_ID, "id": DRAFT_ID, "to": None})
        req = self.last_request()
        assert (req["method"], req["url"], req["json"]) == (
            "patch",
            f"{base}/{DRAFT_ID}",
            {"to": None},
        )

        resend.Inboxes.Drafts.remove(INBOX_ID, DRAFT_ID)
        req = self.last_request()
        assert (req["method"], req["url"]) == ("delete", f"{base}/{DRAFT_ID}")

        resend.Inboxes.Drafts.send(INBOX_ID, DRAFT_ID)
        req = self.last_request()
        assert (req["method"], req["url"]) == ("post", f"{base}/{DRAFT_ID}/send")
