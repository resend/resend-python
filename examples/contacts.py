import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# replace with some audience id
audience_id: str = "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e"
contact_id: str = "b5c95127-937b-4872-a765-06636e5f73da"

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
    "id": contact_id,
    "unsubscribed": False,
    "first_name": "Steve",
}

updated: resend.Contact = resend.Contacts.update(update_params)
print("updated contact !")
print(updated)

cont: resend.Contact = resend.Contacts.get(audience_id=audience_id, id=contact["id"])
print("Retrieved contact")
print(cont)

contacts: resend.Contacts.ListResponse = resend.Contacts.list(audience_id=audience_id)
print("List of contacts")
for contact in contacts["data"]:
    print(contact)

# remove by email
rmed = resend.Contacts.remove(audience_id=audience_id, email=cont["email"])

# remove by id
# rmed: resend.Contact = resend.Contacts.remove(audience_id=audience_id, id=cont["id"])

print(f"Removed contact")
print(rmed)
