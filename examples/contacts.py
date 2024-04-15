import os

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

contact = resend.Contacts.create(create_params)
print(f'Created contact with ID: {contact.id}')

# update_params = {
#     "audience_id": audience_id,
#     "id": contact["id"],
#     "last_name": "Updated",
#     "unsubscribed": False,
# }

# updated = resend.Contacts.update(update_params)
# print("updated contact !")
# print(updated)

# cont = resend.Contacts.get(audience_id=audience_id, id=contact["id"])
# print(cont)

contacts = resend.Contacts.list(audience_id=audience_id)
print("List of contacts")
for contact in contacts:
    print(f'ID: {contact.id}, Email: {contact.email}, First Name: {contact.first_name}, Last Name: {contact.last_name}, Created At: {contact.created_at}, Unsubscribed: {contact.unsubscribed}')

# remove by email
# rmed = resend.Contacts.remove(audience_id=audience_id, email="sw@example.com")

# remove by id
# rmed = resend.Contacts.remove(audience_id=audience_id, id=contact["id"])
# print(rmed)
