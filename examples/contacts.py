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

contact: resend.Contact = resend.Contacts.create(create_params)
print("Created contact !")
print(contact)

update_params: resend.Contacts.UpdateParams = {
    "audience_id": audience_id,
    "id": contact["id"],
    "unsubscribed": False,
    "first_name": "Steve",
}

updated: resend.Contact = resend.Contacts.update(update_params)
print("updated contact !")
print(updated)

cont_by_id: resend.Contact = resend.Contacts.get(
    email=contact["id"], audience_id=audience_id
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
for contact in contacts["data"]:
    print(contact)

# remove by email
rmed = resend.Contacts.remove(audience_id=audience_id, email=contact["email"])

# remove by id
# rmed: resend.Contact = resend.Contacts.remove(audience_id=audience_id, id=cont["id"])

print(f"Removed contact")
print(rmed)
