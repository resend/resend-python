import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

create_params: resend.ApiKeys.CreateParams = {
    "name": "example.com",
}

key: resend.ApiKeys.CreateResponse = resend.ApiKeys.create(params=create_params)
print("Created new api key")
print(f"Key id: {key['id']} and token: {key['token']}")

keys: resend.ApiKeys.ListResponse = resend.ApiKeys.list()
for k in keys["data"]:
    print(k["id"])
    print(k["name"])
    print(k["created_at"])

if len(keys) > 0:
    resend.ApiKeys.remove(api_key_id=keys["data"][0]["id"])
