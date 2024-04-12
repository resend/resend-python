import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


key = resend.ApiKeys.create({"name": "asda"})
print("Created new api key")
print(f'Key id: {key.id} and token: {key.token}')

keys = resend.ApiKeys.list()
for key in keys:
    print(key.id)
    print(key.name)
    print(key.created_at)

try:
    resend.ApiKeys.remove(keys[0].id)
except resend.exceptions.ResendError as e:
    print(e)
