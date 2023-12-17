import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


contact = resend.Contacts.create(
    {
        "audience_id": "48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8",
        "email": "steve.wozniak@gmail.com",
        "first_name": "Steve",
        "last_name": "Wozniak",
        "unsubscribed": True,
    }
)
print(contact)

cont = resend.Contacts.get(
    audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8", id=contact["id"]
)
print(cont)

contacts = resend.Contacts.list(audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8")
print(contacts)

rmed = resend.Contacts.remove(
    audience_id="48c269ed-9873-4d60-bdd9-cd7e6fc0b9b8", id=contact["id"]
)
print(rmed)
