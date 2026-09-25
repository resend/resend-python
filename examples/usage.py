import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

usage: resend.Usage.GetResponse = resend.Usage.get()

print(f"Daily emails used: {usage['emails']['daily']['used']}")
print(f"Monthly emails used: {usage['emails']['monthly']['used']}")
print(f"Contacts used: {usage['contacts']['used']}")
print(f"Rate limit: {usage['rate_limit']['limit']} per {usage['rate_limit']['duration']}")
