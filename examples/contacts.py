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

contact: resend.Contacts.CreateResponse = resend.Contacts.create(create_params)
print("Created contact !")
print(contact)

update_params: resend.Contacts.UpdateParams = {
    "audience_id": audience_id,
    "id": contact["id"],
    "unsubscribed": False,
    "first_name": "Steve1",
}

updated: resend.Contacts.CreateResponse = resend.Contacts.update(update_params)
print("updated contact !")
print(updated)

cont: resend.Contact = resend.Contacts.get(audience_id=audience_id, id=contact["id"])
print("Retrieved contact")
print(cont)

contacts: resend.Contacts.ListResponse = resend.Contacts.list(audience_id=audience_id)
print("List of contacts")
for c in contacts["data"]:
    print(c)

# remove by email
rmed: resend.Contacts.RemoveResponse = resend.Contacts.remove(
    audience_id=audience_id, email=cont["email"]
)

# remove by id
# rmed: resend.Contact = resend.Contacts.remove(audience_id=audience_id, id=cont["id"])

print(f"Removed contact")
print(rmed)
