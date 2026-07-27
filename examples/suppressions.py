import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


# Add: stop delivering to an address.
add_params: resend.Suppressions.AddParams = {
    "email": "blocked@example.com",
}
added = resend.Suppressions.add(add_params)
print(f"Added suppression: {added['id']}")

# List: page through suppressions, optionally filtered by origin.
list_params: resend.Suppressions.ListParams = {
    "origin": "bounce",
    "limit": 10,
}
suppressions = resend.Suppressions.list(list_params)
print(f"Has more: {suppressions['has_more']}")
for suppression in suppressions["data"]:
    print(
        f"{suppression['email']} ({suppression['origin']}) "
        f"source_id={suppression['source_id']}"
    )

# Get: look up a suppression by ID or by email address.
found: resend.Suppression = resend.Suppressions.get("blocked@example.com")
print(f"Suppressed at: {found['created_at']}")

# Batch add: suppress up to 100 addresses in a single call.
batch_add_params: resend.Suppressions.Batch.AddParams = {
    "emails": ["one@example.com", "two@example.com"],
}
batch_added = resend.Suppressions.Batch.add(batch_add_params)
print(f"Batch added {len(batch_added['data'])} suppressions")

# Batch remove: pass either emails or ids, never both.
batch_remove_params: resend.Suppressions.Batch.RemoveParams = {
    "ids": [entry["id"] for entry in batch_added["data"]],
}
batch_removed = resend.Suppressions.Batch.remove(batch_remove_params)
print(f"Batch removed {len(batch_removed['data'])} suppressions")

# Remove: resume delivering to an address.
removed = resend.Suppressions.remove("blocked@example.com")
print(f"Removed suppression {removed['id']}: deleted={removed['deleted']}")
