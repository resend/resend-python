import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest
from tests.inboxes_test import (DRAFT, DRAFT_ID, EMAIL_ID, INBOX, INBOX_ID,
                                LABEL_ID, SENT_EMAIL_ID, THREAD, THREAD_EMAIL,
                                THREAD_ID, THREAD_SUMMARY)

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendInboxesAsync(AsyncResendBaseTest):
    async def test_inboxes_create_async(self) -> None:
        self.set_mock_json({"object": "inbox", "id": INBOX_ID})
        inbox: resend.Inboxes.CreateResponse = await resend.Inboxes.create_async(
            {"email_address": "support@acme.com"}
        )
        assert inbox["id"] == INBOX_ID

    async def test_should_create_inboxes_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.create_async({"email_address": "support@acme.com"})

    async def test_inboxes_list_async(self) -> None:
        self.set_mock_json({"object": "list", "has_more": False, "data": []})
        inboxes: resend.Inboxes.ListResponse = await resend.Inboxes.list_async()
        assert inboxes["object"] == "list"
        assert inboxes["data"] == []

    async def test_should_list_inboxes_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.list_async()

    async def test_inboxes_get_async(self) -> None:
        self.set_mock_json(INBOX)
        inbox: resend.Inbox = await resend.Inboxes.get_async("support@acme.com")
        assert inbox["email_address"] == "support@acme.com"

    async def test_should_get_inboxes_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.get_async(INBOX_ID)

    async def test_inboxes_update_async(self) -> None:
        self.set_mock_json({"object": "inbox", "id": INBOX_ID})
        inbox: resend.Inboxes.UpdateResponse = await resend.Inboxes.update_async(
            {"id": INBOX_ID, "name": "Support"}
        )
        assert inbox["id"] == INBOX_ID

    async def test_should_update_inboxes_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.update_async({"id": INBOX_ID, "name": "Support"})

    async def test_inboxes_remove_async(self) -> None:
        self.set_mock_json({"object": "inbox", "id": INBOX_ID, "deleted": True})
        removed: resend.Inboxes.RemoveResponse = await resend.Inboxes.remove_async(
            INBOX_ID
        )
        assert removed["deleted"] is True

    async def test_should_remove_inboxes_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.remove_async(INBOX_ID)


class TestResendInboxAgentAsync(AsyncResendBaseTest):
    async def test_inbox_agent_get_async(self) -> None:
        self.set_mock_json(
            {
                "object": "inbox_agent",
                "instructions": "Escalate legal threats.",
                "tone": None,
                "enabled_actions": ["draft_reply"],
            }
        )
        agent: resend.InboxAgentSettings = await resend.Inboxes.Agent.get_async(
            INBOX_ID
        )
        assert agent["enabled_actions"] == ["draft_reply"]

    async def test_should_get_inbox_agent_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Agent.get_async(INBOX_ID)

    async def test_inbox_agent_update_async(self) -> None:
        self.set_mock_json(
            {"object": "inbox_agent", "id": "a1f84a4e-6f2b-4f0a-9c1d-8a2e5b3c7d90"}
        )
        agent: resend.Inboxes.Agent.UpdateResponse = (
            await resend.Inboxes.Agent.update_async(
                {"inbox_id": INBOX_ID, "enabled_actions": []}
            )
        )
        assert agent["object"] == "inbox_agent"

    async def test_should_update_inbox_agent_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Agent.update_async(
                {"inbox_id": INBOX_ID, "tone": None}
            )


class TestResendInboxLabelsAsync(AsyncResendBaseTest):
    async def test_inbox_labels_list_async(self) -> None:
        self.set_mock_json({"object": "list", "data": []})
        labels: resend.Inboxes.Labels.ListResponse = (
            await resend.Inboxes.Labels.list_async(INBOX_ID)
        )
        assert labels["data"] == []

    async def test_should_list_inbox_labels_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Labels.list_async(INBOX_ID)

    async def test_inbox_labels_create_async(self) -> None:
        self.set_mock_json({"object": "inbox_label", "id": LABEL_ID})
        label: resend.Inboxes.Labels.CreateResponse = (
            await resend.Inboxes.Labels.create_async(
                {"inbox_id": INBOX_ID, "name": "Urgent"}
            )
        )
        assert label["id"] == LABEL_ID

    async def test_should_create_inbox_labels_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Labels.create_async(
                {"inbox_id": INBOX_ID, "name": "Urgent"}
            )

    async def test_inbox_labels_update_async(self) -> None:
        self.set_mock_json({"object": "inbox_label", "id": LABEL_ID})
        label: resend.Inboxes.Labels.UpdateResponse = (
            await resend.Inboxes.Labels.update_async(
                {"inbox_id": INBOX_ID, "id": LABEL_ID, "color": "#F76B15"}
            )
        )
        assert label["id"] == LABEL_ID

    async def test_should_update_inbox_labels_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Labels.update_async(
                {"inbox_id": INBOX_ID, "id": LABEL_ID, "name": "Billing"}
            )

    async def test_inbox_labels_remove_async(self) -> None:
        self.set_mock_json({"object": "inbox_label", "id": LABEL_ID, "deleted": True})
        removed: resend.Inboxes.Labels.RemoveResponse = (
            await resend.Inboxes.Labels.remove_async(INBOX_ID, LABEL_ID)
        )
        assert removed["deleted"] is True

    async def test_should_remove_inbox_labels_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Labels.remove_async(INBOX_ID, LABEL_ID)


class TestResendInboxThreadsAsync(AsyncResendBaseTest):
    async def test_inbox_threads_list_async(self) -> None:
        self.set_mock_json({"object": "list", "has_more": False, "data": [THREAD]})
        threads: resend.Inboxes.Threads.ListResponse = (
            await resend.Inboxes.Threads.list_async(INBOX_ID, {"labels": [LABEL_ID]})
        )
        assert threads["data"][0]["id"] == THREAD_ID

    async def test_should_list_inbox_threads_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.list_async(INBOX_ID)

    async def test_inbox_threads_search_async(self) -> None:
        result = dict(THREAD)
        result["matched_email_id"] = None
        result["highlights"] = {}
        self.set_mock_json({"object": "list", "has_more": False, "data": [result]})
        threads: resend.Inboxes.Threads.SearchResponse = (
            await resend.Inboxes.Threads.search_async(INBOX_ID, {"query": "refund"})
        )
        assert threads["data"][0]["matched_email_id"] is None
        assert threads["data"][0]["highlights"] == {}

    async def test_should_search_inbox_threads_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.search_async(INBOX_ID)

    async def test_inbox_threads_get_async(self) -> None:
        self.set_mock_json(THREAD_SUMMARY)
        thread: resend.InboxThreadSummary = await resend.Inboxes.Threads.get_async(
            INBOX_ID, THREAD_ID
        )
        assert thread["object"] == "inbox_thread"

    async def test_should_get_inbox_threads_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.get_async(INBOX_ID, THREAD_ID)

    async def test_inbox_threads_update_async(self) -> None:
        self.set_mock_json(THREAD_SUMMARY)
        thread: resend.InboxThreadSummary = await resend.Inboxes.Threads.update_async(
            {"inbox_id": INBOX_ID, "id": THREAD_ID, "remove_label_ids": [LABEL_ID]}
        )
        assert thread["id"] == THREAD_ID

    async def test_should_update_inbox_threads_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.update_async(
                {"inbox_id": INBOX_ID, "id": THREAD_ID, "read": True}
            )

    async def test_inbox_threads_remove_async(self) -> None:
        self.set_mock_json(
            {"object": "inbox_thread", "id": THREAD_ID, "deleted": False}
        )
        removed: resend.Inboxes.Threads.RemoveResponse = (
            await resend.Inboxes.Threads.remove_async(INBOX_ID, THREAD_ID)
        )
        assert removed["deleted"] is False

    async def test_should_remove_inbox_threads_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.remove_async(INBOX_ID, THREAD_ID)


class TestResendInboxThreadEmailsAsync(AsyncResendBaseTest):
    async def test_inbox_thread_emails_list_async(self) -> None:
        self.set_mock_json({"object": "list", "has_more": False, "data": [THREAD_EMAIL]})
        emails: resend.Inboxes.Threads.Emails.ListResponse = (
            await resend.Inboxes.Threads.Emails.list_async(INBOX_ID, THREAD_ID)
        )
        assert emails["data"][0]["id"] == EMAIL_ID

    async def test_should_list_inbox_thread_emails_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.Emails.list_async(INBOX_ID, THREAD_ID)

    async def test_inbox_thread_emails_get_async(self) -> None:
        self.set_mock_json(THREAD_EMAIL)
        email: resend.InboxThreadEmail = await resend.Inboxes.Threads.Emails.get_async(
            INBOX_ID, THREAD_ID, EMAIL_ID
        )
        assert email["id"] == EMAIL_ID

    async def test_should_get_inbox_thread_emails_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.Emails.get_async(
                INBOX_ID, THREAD_ID, EMAIL_ID
            )

    async def test_inbox_thread_emails_reply_async(self) -> None:
        self.set_mock_json({"id": SENT_EMAIL_ID})
        reply: resend.Inboxes.Threads.Emails.ReplyResponse = (
            await resend.Inboxes.Threads.Emails.reply_async(
                {
                    "inbox_id": INBOX_ID,
                    "thread_id": THREAD_ID,
                    "email_id": EMAIL_ID,
                    "text": "Refund issued for order 1041.",
                }
            )
        )
        assert reply["id"] == SENT_EMAIL_ID

    async def test_should_reply_inbox_thread_emails_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.Emails.reply_async(
                {
                    "inbox_id": INBOX_ID,
                    "thread_id": THREAD_ID,
                    "email_id": EMAIL_ID,
                    "html": "<p>Hi</p>",
                }
            )

    async def test_inbox_thread_emails_forward_async(self) -> None:
        self.set_mock_json({"id": SENT_EMAIL_ID})
        forward: resend.Inboxes.Threads.Emails.ForwardResponse = (
            await resend.Inboxes.Threads.Emails.forward_async(
                {
                    "inbox_id": INBOX_ID,
                    "thread_id": THREAD_ID,
                    "email_id": EMAIL_ID,
                    "to": ["colleague@example.org"],
                }
            )
        )
        assert forward["id"] == SENT_EMAIL_ID

    async def test_should_forward_inbox_thread_emails_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Threads.Emails.forward_async(
                {
                    "inbox_id": INBOX_ID,
                    "thread_id": THREAD_ID,
                    "email_id": EMAIL_ID,
                    "to": "colleague@example.org",
                }
            )


class TestResendInboxDraftsAsync(AsyncResendBaseTest):
    async def test_inbox_drafts_list_async(self) -> None:
        self.set_mock_json({"object": "list", "has_more": False, "data": []})
        drafts: resend.Inboxes.Drafts.ListResponse = (
            await resend.Inboxes.Drafts.list_async(INBOX_ID)
        )
        assert drafts["data"] == []

    async def test_should_list_inbox_drafts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Drafts.list_async(INBOX_ID)

    async def test_inbox_drafts_create_async(self) -> None:
        self.set_mock_json({"object": "inbox_draft", "id": DRAFT_ID})
        draft: resend.Inboxes.Drafts.CreateResponse = (
            await resend.Inboxes.Drafts.create_async(
                {"inbox_id": INBOX_ID, "to": "ada@example.org", "text": "Hi"}
            )
        )
        assert draft["id"] == DRAFT_ID

    async def test_should_create_inbox_drafts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Drafts.create_async(
                {"inbox_id": INBOX_ID, "text": "Hi"}
            )

    async def test_inbox_drafts_get_async(self) -> None:
        self.set_mock_json(DRAFT)
        draft: resend.InboxDraft = await resend.Inboxes.Drafts.get_async(
            INBOX_ID, DRAFT_ID
        )
        assert draft["id"] == DRAFT_ID

    async def test_should_get_inbox_drafts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Drafts.get_async(INBOX_ID, DRAFT_ID)

    async def test_inbox_drafts_update_async(self) -> None:
        self.set_mock_json(DRAFT)
        draft: resend.InboxDraft = await resend.Inboxes.Drafts.update_async(
            {"inbox_id": INBOX_ID, "id": DRAFT_ID, "subject": "Refund for order 1041"}
        )
        assert draft["subject"] == "Refund for order 1041"

    async def test_should_update_inbox_drafts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Drafts.update_async(
                {"inbox_id": INBOX_ID, "id": DRAFT_ID, "text": None}
            )

    async def test_inbox_drafts_remove_async(self) -> None:
        self.set_mock_json({"object": "inbox_draft", "id": DRAFT_ID, "deleted": True})
        removed: resend.Inboxes.Drafts.RemoveResponse = (
            await resend.Inboxes.Drafts.remove_async(INBOX_ID, DRAFT_ID)
        )
        assert removed["deleted"] is True

    async def test_should_remove_inbox_drafts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Drafts.remove_async(INBOX_ID, DRAFT_ID)

    async def test_inbox_drafts_send_async(self) -> None:
        self.set_mock_json({"id": SENT_EMAIL_ID})
        sent: resend.Inboxes.Drafts.SendResponse = (
            await resend.Inboxes.Drafts.send_async(INBOX_ID, DRAFT_ID)
        )
        assert sent["id"] == SENT_EMAIL_ID

    async def test_should_send_inbox_drafts_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.Inboxes.Drafts.send_async(INBOX_ID, DRAFT_ID)


class TestInboxesAsyncPaths(AsyncResendBaseTest):
    def last_url(self) -> str:
        return str(self.mock.call_args.kwargs["url"])

    async def test_every_async_method_calls_its_path(self) -> None:
        self.set_mock_json({"object": "inbox", "id": INBOX_ID})
        api = "https://api.resend.com"
        inbox = f"{api}/inboxes/{INBOX_ID}"
        thread = f"{inbox}/threads/{THREAD_ID}"
        email = f"{thread}/emails/{EMAIL_ID}"
        draft = f"{inbox}/drafts/{DRAFT_ID}"

        await resend.Inboxes.create_async({"email_address": "support@acme.com"})
        assert self.last_url() == f"{api}/inboxes"
        await resend.Inboxes.list_async({"limit": 1})
        assert self.last_url() == f"{api}/inboxes?limit=1"
        await resend.Inboxes.get_async("support@acme.com")
        assert self.last_url() == f"{api}/inboxes/support%40acme.com"
        await resend.Inboxes.update_async({"id": INBOX_ID, "name": "Support"})
        assert self.last_url() == inbox
        await resend.Inboxes.remove_async(INBOX_ID)
        assert self.last_url() == inbox

        await resend.Inboxes.Agent.get_async(INBOX_ID)
        assert self.last_url() == f"{inbox}/agent"
        await resend.Inboxes.Agent.update_async({"inbox_id": INBOX_ID, "tone": None})
        assert self.last_url() == f"{inbox}/agent"

        await resend.Inboxes.Labels.list_async(INBOX_ID)
        assert self.last_url() == f"{inbox}/labels"
        await resend.Inboxes.Labels.create_async({"inbox_id": INBOX_ID, "name": "Urgent"})
        assert self.last_url() == f"{inbox}/labels"
        await resend.Inboxes.Labels.update_async(
            {"inbox_id": INBOX_ID, "id": LABEL_ID, "name": "Billing"}
        )
        assert self.last_url() == f"{inbox}/labels/{LABEL_ID}"
        await resend.Inboxes.Labels.remove_async(INBOX_ID, LABEL_ID)
        assert self.last_url() == f"{inbox}/labels/{LABEL_ID}"

        await resend.Inboxes.Threads.list_async(
            INBOX_ID, {"folders": ["inbox", "sent"], "read": True}
        )
        assert self.last_url() == f"{inbox}/threads?folders=inbox%2Csent&read=true"
        await resend.Inboxes.Threads.search_async(
            INBOX_ID, {"to": ["a@example.com"], "has_attachment": False}
        )
        assert (
            self.last_url()
            == f"{inbox}/threads/search?to=a%40example.com&has_attachment=false"
        )
        await resend.Inboxes.Threads.get_async(INBOX_ID, THREAD_ID)
        assert self.last_url() == thread
        await resend.Inboxes.Threads.update_async(
            {"inbox_id": INBOX_ID, "id": THREAD_ID, "read": True}
        )
        assert self.last_url() == thread
        await resend.Inboxes.Threads.remove_async(INBOX_ID, THREAD_ID)
        assert self.last_url() == thread

        await resend.Inboxes.Threads.Emails.list_async(
            INBOX_ID, THREAD_ID, {"after": EMAIL_ID}
        )
        assert self.last_url() == f"{thread}/emails?after={EMAIL_ID}"
        await resend.Inboxes.Threads.Emails.get_async(INBOX_ID, THREAD_ID, EMAIL_ID)
        assert self.last_url() == email
        await resend.Inboxes.Threads.Emails.reply_async(
            {"inbox_id": INBOX_ID, "thread_id": THREAD_ID, "email_id": EMAIL_ID, "text": "Hi"}
        )
        assert self.last_url() == f"{email}/reply"
        await resend.Inboxes.Threads.Emails.forward_async(
            {
                "inbox_id": INBOX_ID,
                "thread_id": THREAD_ID,
                "email_id": EMAIL_ID,
                "to": "colleague@example.org",
            }
        )
        assert self.last_url() == f"{email}/forward"

        await resend.Inboxes.Drafts.list_async(INBOX_ID, {"limit": 1})
        assert self.last_url() == f"{inbox}/drafts?limit=1"
        await resend.Inboxes.Drafts.create_async({"inbox_id": INBOX_ID, "text": "Hi"})
        assert self.last_url() == f"{inbox}/drafts"
        await resend.Inboxes.Drafts.get_async(INBOX_ID, DRAFT_ID)
        assert self.last_url() == draft
        await resend.Inboxes.Drafts.update_async(
            {"inbox_id": INBOX_ID, "id": DRAFT_ID, "text": "Hello"}
        )
        assert self.last_url() == draft
        await resend.Inboxes.Drafts.remove_async(INBOX_ID, DRAFT_ID)
        assert self.last_url() == draft
        await resend.Inboxes.Drafts.send_async(INBOX_ID, DRAFT_ID)
        assert self.last_url() == f"{draft}/send"
