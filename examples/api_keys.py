import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

create_params: resend.ApiKeys.CreateParams = {
    "name": "example.com",
}

created_key: resend.ApiKeys.CreateApiKeyResponse = resend.ApiKeys.create(
    params=create_params
)
print("Created new api key")
print(f"Key id: {created_key['id']} and token: {created_key['token']}")

keys: resend.ApiKeys.ListResponse = resend.ApiKeys.list()
for key in keys["data"]:
    print(key["id"])
    print(key["name"])
    print(key["created_at"])

print("\n--- Using pagination parameters ---")
if keys["data"]:
    paginated_params: resend.ApiKeys.ListParams = {
        "limit": 8,
        "after": keys["data"][0]["id"]
    }
    paginated_keys: resend.ApiKeys.ListResponse = resend.ApiKeys.list(params=paginated_params)
    print(f"Retrieved {len(paginated_keys['data'])} keys with pagination")
    print(f"Has more keys: {paginated_keys['has_more']}")
else:
    print("No keys available for pagination example")

if len(keys["data"]) > 0:
    resend.ApiKeys.remove(api_key_id=keys["data"][0]["id"])
