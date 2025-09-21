import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# replace with some audience id
audience_id: str = "ca4e37c5-a82a-4199-a3b8-bf912a6472aa"

create_params: resend.Contacts.CreateParams = {
    "audience_id": audience_id,
    "email": "sw@exmple.com",
    "first_name": "Steve",
    "last_name": "Wozniak",
    "unsubscribed": False,
}

contact: resend.Contacts.CreateContactResponse = resend.Contacts.create(create_params)
print("Created contact with ID: {}".format(contact["id"]))
print(contact)

update_params: resend.Contacts.UpdateParams = {
    "audience_id": audience_id,
    "id": contact["id"],
    "unsubscribed": False,
    "first_name": "Steve",
}

updated: resend.Contacts.UpdateContactResponse = resend.Contacts.update(update_params)
print("updated contact with ID: {}".format(updated["id"]))
print(updated)

cont_by_id: resend.Contact = resend.Contacts.get(
    id=contact["id"], audience_id=audience_id
)
print("Retrieved contact by ID")
print(cont_by_id)

cont_by_email: resend.Contact = resend.Contacts.get(
    email="sw@exmple.com", audience_id=audience_id
)
print("Retrieved contact by Email")
print(cont_by_email)

contacts: resend.Contacts.ListResponse = resend.Contacts.list(audience_id=audience_id)
print("List of contacts")
print(f"Found {len(contacts['data'])} contacts")
print(f"Has more contacts: {contacts['has_more']}")
for c in contacts["data"]:
    print(c)

print("\n--- Using pagination parameters ---")
if contacts["data"]:
    paginated_params: resend.Contacts.ListParams = {
        "limit": 2,
        "after": contacts["data"][0]["id"]
    }
    paginated_contacts: resend.Contacts.ListResponse = resend.Contacts.list(
        audience_id=audience_id, params=paginated_params
    )
    print(f"Retrieved {len(paginated_contacts['data'])} contacts with pagination")
    print(f"Has more contacts: {paginated_contacts['has_more']}")
else:
    print("No contacts available for pagination example")

# remove by email
rmed: resend.Contacts.RemoveContactResponse = resend.Contacts.remove(
    audience_id=audience_id, email=cont_by_email["email"]
)

# remove by id
# rmed: resend.Contacts.RemoveContactResponse = resend.Contacts.remove(audience_id=audience_id, id=cont["id"])

print(f"Removed contact with ID: {rmed['contact']}")
print(rmed)
