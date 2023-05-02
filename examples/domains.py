import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


resend.api_key = os.environ["RESEND_API_KEY"]

domain = resend.Domains.create(
    {
        "name": "domain.io",
    }
)
print(domain)

domains = resend.Domains.list()
print(domains)

resend.Domains.verify(domain_id=domain["id"])
print("domain verified")

resend.Domains.remove(domain_id=domain["id"])
print("domain removed")
