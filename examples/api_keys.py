import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

create_params: resend.ApiKeys.CreateParams = {
    "name": "example.com",
}

key: resend.ApiKey = resend.ApiKeys.create(params=create_params)
print("Created new api key")
print(f"Key id: {key.id} and token: {key.token}")

keys: List[resend.ApiKey] = resend.ApiKeys.list()
for key in keys:
    print(key.id)
    print(key.name)
    print(key.created_at)

if len(keys) > 0:
    resend.ApiKeys.remove(api_key_id=keys[0].id)
