import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


async def main() -> None:
    created: resend.Inboxes.CreateResponse = await resend.Inboxes.create_async(
        {"email_address": "support@acme.com", "name": "Customer Support"}
    )
    inbox_id = created["id"]
    print(f"Created inbox: {inbox_id}")

    inbox: resend.Inbox = await resend.Inboxes.get_async(inbox_id)
    print(f"Retrieved inbox: {inbox['email_address']}")

    label: resend.Inboxes.Labels.CreateResponse = (
        await resend.Inboxes.Labels.create_async(
            {"inbox_id": inbox_id, "name": "Urgent", "color": "#E93D82"}
        )
    )

    threads: resend.Inboxes.Threads.SearchResponse = (
        await resend.Inboxes.Threads.search_async(
            inbox_id, {"query": "refund", "folders": ["inbox"]}
        )
    )
    print(f"Found {len(threads['data'])} matching threads")

    if threads["data"]:
        thread_id = threads["data"][0]["id"]
        await resend.Inboxes.Threads.update_async(
            {"inbox_id": inbox_id, "id": thread_id, "add_label_ids": [label["id"]]}
        )
        emails: resend.Inboxes.Threads.Emails.ListResponse = (
            await resend.Inboxes.Threads.Emails.list_async(inbox_id, thread_id)
        )
        reply: resend.Inboxes.Threads.Emails.ReplyResponse = (
            await resend.Inboxes.Threads.Emails.reply_async(
                {
                    "inbox_id": inbox_id,
                    "thread_id": thread_id,
                    "email_id": emails["data"][-1]["id"],
                    "text": "Thanks, we are on it.",
                }
            )
        )
        print(f"Sent reply: {reply['id']}")

    draft: resend.Inboxes.Drafts.CreateResponse = (
        await resend.Inboxes.Drafts.create_async(
            {"inbox_id": inbox_id, "to": "ada@example.org", "text": "Hello"}
        )
    )
    sent: resend.Inboxes.Drafts.SendResponse = await resend.Inboxes.Drafts.send_async(
        inbox_id, draft["id"]
    )
    print(f"Sent draft as email: {sent['id']}")

    await resend.Inboxes.Labels.remove_async(inbox_id, label["id"])
    await resend.Inboxes.remove_async(inbox_id)


if __name__ == "__main__":
    asyncio.run(main())
