import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

create_params: resend.Inboxes.CreateParams = {
    "email_address": "support@acme.com",
    "name": "Customer Support",
    "from_name": "Ada from Support",
}
created: resend.Inboxes.CreateResponse = resend.Inboxes.create(create_params)
inbox_id = created["id"]
print(f"Created inbox: {inbox_id}")

inbox: resend.Inbox = resend.Inboxes.get("support@acme.com")
print(f"Retrieved inbox {inbox['email_address']} with {inbox['unread']} unread threads")

inboxes: resend.Inboxes.ListResponse = resend.Inboxes.list({"limit": 10})
print(f"Found {len(inboxes['data'])} inboxes")

update_params: resend.Inboxes.UpdateParams = {"id": inbox_id, "name": "Support"}
resend.Inboxes.update(update_params)

agent: resend.InboxAgentSettings = resend.Inboxes.Agent.get(inbox_id)
print(f"Agent actions: {agent['actions']}")
agent_params: resend.Inboxes.Agent.UpdateParams = {
    "inbox_id": inbox_id,
    "tone": "concise_casual",
    "actions": ["draft_reply", "add_labels"],
}
resend.Inboxes.Agent.update(agent_params)

label_params: resend.Inboxes.Labels.CreateParams = {
    "inbox_id": inbox_id,
    "name": "Urgent",
    "color": "#E93D82",
}
label: resend.Inboxes.Labels.CreateResponse = resend.Inboxes.Labels.create(
    label_params
)
label_update: resend.Inboxes.Labels.UpdateParams = {
    "inbox_id": inbox_id,
    "id": label["id"],
    "color": "#F76B15",
}
resend.Inboxes.Labels.update(label_update)
labels: resend.Inboxes.Labels.ListResponse = resend.Inboxes.Labels.list(inbox_id)
print(f"Found {len(labels['data'])} labels")

threads: resend.Inboxes.Threads.ListResponse = resend.Inboxes.Threads.list(
    inbox_id, {"folders": ["inbox", "sent"], "read": False, "limit": 10}
)
print(f"Found {len(threads['data'])} unread threads")

search_params: resend.Inboxes.Threads.SearchParams = {
    "query": "refund",
    "has_attachment": False,
}
results: resend.Inboxes.Threads.SearchResponse = resend.Inboxes.Threads.search(
    inbox_id, search_params
)
for result in results["data"]:
    print(f"{result['subject']}: matched email {result['matched_email_id']}")

if threads["data"]:
    thread_id = threads["data"][0]["id"]
    thread: resend.InboxThreadSummary = resend.Inboxes.Threads.get(inbox_id, thread_id)
    print(f"Thread {thread['id']} is in {thread['folder']}")

    thread_update: resend.Inboxes.Threads.UpdateParams = {
        "inbox_id": inbox_id,
        "id": thread_id,
        "read": True,
    }
    resend.Inboxes.Threads.update(thread_update)

    add_labels: resend.Inboxes.Threads.Labels.AddParams = {
        "inbox_id": inbox_id,
        "thread_id": thread_id,
        "labels": [label["id"]],
    }
    thread_labels: resend.Inboxes.Threads.Labels.ListResponse = (
        resend.Inboxes.Threads.Labels.add(add_labels)
    )
    print(f"Thread has {len(thread_labels['data'])} labels")
    resend.Inboxes.Threads.Labels.remove(inbox_id, thread_id, label["id"])

    emails: resend.Inboxes.Threads.Emails.ListResponse = (
        resend.Inboxes.Threads.Emails.list(inbox_id, thread_id)
    )
    email_id = emails["data"][0]["id"]
    email: resend.InboxThreadEmail = resend.Inboxes.Threads.Emails.get(
        inbox_id, thread_id, email_id
    )
    print(f"First email from {email['from']}: {email['subject']}")

    reply_params: resend.Inboxes.Threads.Emails.ReplyParams = {
        "inbox_id": inbox_id,
        "thread_id": thread_id,
        "email_id": email_id,
        "text": "Thanks, we are on it.",
        "attachments": [{"filename": "note.txt", "content": "VGhhbmtzIQ=="}],
    }
    reply: resend.Inboxes.Threads.Emails.ReplyResponse = (
        resend.Inboxes.Threads.Emails.reply(reply_params)
    )
    print(f"Sent reply: {reply['id']}")

    forward_params: resend.Inboxes.Threads.Emails.ForwardParams = {
        "inbox_id": inbox_id,
        "thread_id": thread_id,
        "email_id": email_id,
        "to": ["colleague@example.org"],
        "text": "Flagging this for you.",
    }
    forward: resend.Inboxes.Threads.Emails.ForwardResponse = (
        resend.Inboxes.Threads.Emails.forward(forward_params)
    )
    print(f"Sent forward: {forward['id']}")

    resend.Inboxes.Threads.remove(inbox_id, thread_id)

draft_params: resend.Inboxes.Drafts.CreateParams = {
    "inbox_id": inbox_id,
    "to": ["ada@example.org"],
    "subject": "Refund for order 1041",
    "text": "Refund issued for order 1041.",
    "attachments": [
        {
            "content": "UmVmdW5kIHJlY2VpcHQ=",
            "filename": "receipt.txt",
            "content_type": "text/plain",
        }
    ],
}
draft: resend.Inboxes.Drafts.CreateResponse = resend.Inboxes.Drafts.create(
    draft_params
)
draft_update: resend.Inboxes.Drafts.UpdateParams = {
    "inbox_id": inbox_id,
    "id": draft["id"],
    "html": "<p>Refund issued for order 1041.</p>",
}
updated: resend.Inboxes.Drafts.UpdateResponse = resend.Inboxes.Drafts.update(
    draft_update
)
updated_draft: resend.InboxDraft = resend.Inboxes.Drafts.get(inbox_id, updated["id"])
print(f"Draft {updated_draft['id']} is a {updated_draft['type']} draft")
print(f"Draft attachments: {[a['filename'] for a in updated_draft['attachments']]}")

drafts: resend.Inboxes.Drafts.ListResponse = resend.Inboxes.Drafts.list(inbox_id)
print(f"Found {len(drafts['data'])} drafts")

send_options: resend.Inboxes.Drafts.SendOptions = {
    "idempotency_key": f"send-draft-{draft['id']}",
}
send_params: resend.Inboxes.Drafts.SendParams = {
    "headers": {"X-Ticket-Id": "4821"},
}
sent: resend.Inboxes.Drafts.SendResponse = resend.Inboxes.Drafts.send(
    inbox_id, draft["id"], send_params, send_options
)
print(f"Sent draft as email: {sent['id']}")

resend.Inboxes.Labels.remove(inbox_id, label["id"])
removed: resend.Inboxes.RemoveResponse = resend.Inboxes.remove(inbox_id)
print(f"Removed inbox: {removed['deleted']}")
