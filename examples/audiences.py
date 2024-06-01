import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Audiences.CreateParams = {
    "name": "New Audience from Python SDK",
}
audience: resend.Audiences.CreateResponse = resend.Audiences.create(create_params)
print(f"Created audience: {audience['id']}")
print(audience)

aud: resend.Audience = resend.Audiences.get(audience["id"])
print("Retrieved audience: ", aud)

audiences: resend.Audiences.ListResponse = resend.Audiences.list()
print("List of audiences:", [a["id"] for a in audiences["data"]])

rmed: resend.Audiences.RemoveResponse = resend.Audiences.remove(id=audience["id"])
print(f"Deleted audience")
print(rmed)
