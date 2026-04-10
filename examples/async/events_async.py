import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


async def main() -> None:
    # Create a contact to use with event sends
    print("--- Create contact ---")
    contact: resend.Contacts.CreateContactResponse = await resend.Contacts.create_async({
        "email": "test-events-async@example.com",
        "first_name": "Test",
        "last_name": "User",
    })
    contact_id = contact["id"]
    print(f"Contact: {contact_id}")

    # --- Create event ---
    print("\n--- Create event ---")
    created: resend.Events.CreateResponse = await resend.Events.create_async({
        "name": "user.signed_up",
        "schema": {
            "plan": "string",
            "trial_days": "number",
            "is_enterprise": "boolean",
            "upgraded_at": "date",
        },
    })
    event_id = created["id"]
    print(f"Created event: {event_id}")

    # --- Get event by ID ---
    print("\n--- Get event by ID ---")
    event: resend.Event = await resend.Events.get_async(event_id)
    print(f"Name: {event['name']}, schema: {event['schema']}")

    # --- Get event by name ---
    print("\n--- Get event by name ---")
    event_by_name: resend.Event = await resend.Events.get_async("user.signed_up")
    print(f"Found by name: {event_by_name['name']}")

    # --- Update event schema ---
    print("\n--- Update event schema ---")
    updated: resend.Events.UpdateResponse = await resend.Events.update_async({
        "identifier": "user.signed_up",
        "schema": {"plan": "string", "source": "string"},
    })
    print(f"Updated event: {updated['id']}")

    # --- Send event with contact_id ---
    print("\n--- Send event with contact_id ---")
    sent: resend.Events.SendResponse = await resend.Events.send_async({
        "event": "user.signed_up",
        "contact_id": contact_id,
        "payload": {"plan": "pro"},
    })
    print(f"Sent event: {sent['event']}")

    # --- Send event with email ---
    print("\n--- Send event with email ---")
    sent_email: resend.Events.SendResponse = await resend.Events.send_async({
        "event": "user.signed_up",
        "email": "test-events-async@example.com",
    })
    print(f"Sent event: {sent_email['event']}")

    # --- List events ---
    print("\n--- List events ---")
    list_resp: resend.Events.ListResponse = await resend.Events.list_async()
    print(f"Total: {len(list_resp['data'])}, has_more: {list_resp['has_more']}")

    # --- Cleanup ---
    print("\n--- Delete event ---")
    deleted: resend.Events.DeleteResponse = await resend.Events.remove_async(event_id)
    print(f"Deleted: {deleted['deleted']}")

    print("\n--- Delete contact ---")
    await resend.Contacts.remove_async(id=contact_id)
    print(f"Deleted contact: {contact_id}")


asyncio.run(main())
