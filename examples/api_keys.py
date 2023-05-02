import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


resend.api_key = os.environ["RESEND_API_KEY"]

key = resend.ApiKeys.create(
    {
        "name": "prod",
    }
)
print(key)

keys = resend.ApiKeys.list()
print(keys)

resend.ApiKeys.remove(key["id"])
