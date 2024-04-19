import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Audiences.CreateParams = {
    "name": "New Audience from Python SDK",
}
audience = resend.Audiences.create(create_params)
print(f"Created audience: {audience.id}")
print(f"{audience.name} created")

aud = resend.Audiences.get(audience.id)
print("Retrieved audience:", aud.id, aud.name, aud.created_at)

audiences = resend.Audiences.list()
print("List of audiences:", [a.id for a in audiences])

rmed = resend.Audiences.remove(id=audience.id)
print(f"Deleted audience: {rmed.id} {rmed.deleted}")
