import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


audience = resend.Audiences.create(
    {
        "name": "New Audience from Python SDK",
    }
)
print(audience)

aud = resend.Audiences.get(audience["id"])
print(aud)

audiences = resend.Audiences.list()
print(audiences)

rmed = resend.Audiences.remove(audience["id"])
print(rmed)
