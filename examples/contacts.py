import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


audience_id = "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e"

contact = resend.Contacts.create(
    {
        "audience_id": audience_id,
        "email": "sw@example.com",
        "first_name": "Steve",
        "last_name": "Wozniak",
        "unsubscribed": True,
    }
)
print("created contact !")
print(contact)

update_params = {
    "audience_id": audience_id,
    "id": contact["id"],
    "last_name": "Updated",
    "unsubscribed": False,
}

updated = resend.Contacts.update(update_params)
print("updated contact !")
print(updated)

cont = resend.Contacts.get(
    audience_id=audience_id, id=contact["id"]
)
print(cont)

contacts = resend.Contacts.list(audience_id=audience_id)
print(contacts)

rmed = resend.Contacts.remove(
    audience_id=audience_id, id=contact["id"]
)
print(rmed)
