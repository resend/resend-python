import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Domains.CreateParams = {
    "name": "drish.dev",
    "region": "us-east-1",
    "custom_return_path": "outbound",
}
domain: resend.Domain = resend.Domains.create(params=create_params)
print(domain)

retrieved: resend.Domain = resend.Domains.get(domain_id=domain["id"])
if retrieved["records"] is not None:
    for record in retrieved["records"]:
        print(record)

update_params: resend.Domains.UpdateParams = {
    "id": domain["id"],
    "open_tracking": True,
    "click_tracking": True,
    "tls": "enforced",
}

updated_domain: resend.Domain = resend.Domains.update(update_params)
print(f"Updated domain: {updated_domain['id']}")

domains: resend.Domains.ListResponse = resend.Domains.list()
if not domains:
    print("No domains found")
for domain in domains["data"]:
    print(domain)

verified_domain: resend.Domain = resend.Domains.verify(domain_id=domain["id"])
print(f"Verified")
print(verified_domain)

rm_domain: resend.Domain = resend.Domains.remove(domain_id=domain["id"])
print(rm_domain)
