import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

print("\nGlobal contacts are organization-wide and support custom properties.")
print("They are not tied to any specific audience.\n")

# Create a global contact with properties
print("\n--- Creating global contact with custom properties ---")
create_params: resend.Contacts.CreateParams = {
    "email": "global.user@example.com",
    "first_name": "Global",
    "last_name": "User",
    "unsubscribed": False,
    "properties": {
        "tier": "premium",
        "role": "admin",
        "signup_source": "website",
    },
}

contact: resend.Contacts.CreateContactResponse = resend.Contacts.create(create_params)
print(f"Created global contact with ID: {contact['id']}")
print(contact)

# Update global contact with new properties
print("\n--- Updating global contact ---")
update_params: resend.Contacts.UpdateParams = {
    "id": contact["id"],
    "first_name": "Updated Global",
    "properties": {
        "tier": "enterprise",  # Update existing property
        "role": "super_admin",  # Update existing property
        "last_login": "2024-01-15",  # Add new property
    },
}

updated: resend.Contacts.UpdateContactResponse = resend.Contacts.update(update_params)
print(f"Updated contact with ID: {updated['id']}")
print(updated)

# Get contact by ID
print("\n--- Retrieving global contact by ID ---")
cont_by_id: resend.Contact = resend.Contacts.get(id=contact["id"])
print("Retrieved contact by ID:")
print(cont_by_id)
if "properties" in cont_by_id:
    print(f"Custom properties: {cont_by_id['properties']}")

# List all global contacts
print("\n--- Listing all global contacts ---")
contacts: resend.Contacts.ListResponse = resend.Contacts.list()
print(f"Found {len(contacts['data'])} global contacts")
print(f"Has more contacts: {contacts['has_more']}")
for c in contacts["data"]:
    print(f"  - {c['email']} (ID: {c['id']})")
    if "properties" in c:
        print(f"    Properties: {c.get('properties')}")

# List with pagination
print("\n--- Using pagination parameters ---")
if contacts["data"]:
    paginated_params: resend.Contacts.ListParams = {
        "limit": 2,
        "after": contacts["data"][0]["id"],
    }
    paginated_contacts: resend.Contacts.ListResponse = resend.Contacts.list(
        params=paginated_params
    )
    print(f"Retrieved {len(paginated_contacts['data'])} contacts with pagination")
    print(f"Has more contacts: {paginated_contacts['has_more']}")
else:
    print("No contacts available for pagination example")

print("\n--- Removing global contact by ID ---")
rmed: resend.Contacts.RemoveContactResponse = resend.Contacts.remove(id=contact["id"])
print(f"Removed contact with ID: {rmed['contact']}")
print(rmed)
