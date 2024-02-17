import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


domain = resend.Domains.create(
    {
        "name": "domain.io",
    }
)
print(domain)

retrieved = resend.Domains.get(domain_id=domain["id"])
print(retrieved)

update_params = {
    "id": domain["id"],
    "open_tracking": True,
    "click_tracking": True,
}

updated = resend.Domains.update(update_params)
print(updated)

domains = resend.Domains.list()
print(domains)

resend.Domains.verify(domain_id=domain["id"])
print("domain verified")

resend.Domains.remove(domain_id=domain["id"])
print("domain removed")
