import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Create a contact to use with event sends
print("--- Create contact ---")
contact: resend.Contacts.CreateContactResponse = resend.Contacts.create({
    "email": "test-events@example.com",
    "first_name": "Test",
    "last_name": "User",
})
contact_id = contact["id"]
print(f"Contact: {contact_id}")

# --- Create event without schema ---
print("\n--- Create event without schema ---")
created: resend.Events.CreateResponse = resend.Events.create({"name": "user.signed_up"})
event_id = created["id"]
print(f"Created event: {event_id}")

# --- Create event with schema ---
print("\n--- Create event with schema ---")
created_with_schema: resend.Events.CreateResponse = resend.Events.create({
    "name": "user.upgraded",
    "schema": {
        "plan": "string",
        "trial_days": "number",
        "is_enterprise": "boolean",
        "upgraded_at": "date",
    },
})
print(f"Created event with schema: {created_with_schema['id']}")

# --- Get event by ID ---
print("\n--- Get event by ID ---")
event: resend.Event = resend.Events.get(event_id)
print(f"ID: {event['id']}")
print(f"Name: {event['name']}")
print(f"Schema: {event['schema']}")

# --- Get event by name ---
print("\n--- Get event by name ---")
event_by_name: resend.Event = resend.Events.get("user.signed_up")
print(f"Found by name: {event_by_name['name']}")

# --- Update event schema ---
print("\n--- Update event schema ---")
updated: resend.Events.UpdateResponse = resend.Events.update({
    "identifier": "user.signed_up",
    "schema": {"plan": "string", "source": "string"},
})
print(f"Updated event: {updated['id']}")

# --- Send event with contact_id ---
print("\n--- Send event with contact_id ---")
sent: resend.Events.SendResponse = resend.Events.send({
    "event": "user.signed_up",
    "contact_id": contact_id,
    "payload": {"plan": "pro", "source": "web"},
})
print(f"Sent event: {sent['event']}")

# --- Send event with email ---
print("\n--- Send event with email ---")
sent_email: resend.Events.SendResponse = resend.Events.send({
    "event": "user.signed_up",
    "email": "test-events@example.com",
})
print(f"Sent event: {sent_email['event']}")

# --- List events ---
print("\n--- List events ---")
list_resp: resend.Events.ListResponse = resend.Events.list()
print(f"Total events: {len(list_resp['data'])}, has_more: {list_resp['has_more']}")
for ev in list_resp["data"]:
    print(f"  {ev['name']} ({ev['id']})")

# --- List events with pagination ---
print("\n--- List events with pagination ---")
paginated: resend.Events.ListResponse = resend.Events.list(params={"limit": 5})
print(f"Retrieved {len(paginated['data'])} events")

# --- Cleanup ---
print("\n--- Delete event by ID ---")
deleted: resend.Events.DeleteResponse = resend.Events.remove(event_id)
print(f"Deleted: {deleted['deleted']}")

print("\n--- Delete event by name ---")
deleted_by_name: resend.Events.DeleteResponse = resend.Events.remove("user.upgraded")
print(f"Deleted by name: {deleted_by_name['deleted']}")

print("\n--- Delete contact ---")
resend.Contacts.remove(id=contact_id)
print(f"Deleted contact: {contact_id}")
