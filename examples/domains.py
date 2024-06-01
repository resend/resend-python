import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Domains.CreateParams = {
    "name": "example.com",
    "region": "us-east-1",
}
domain: resend.Domains.CreateResponse = resend.Domains.create(params=create_params)
print(domain)

retrieved: resend.Domain = resend.Domains.get(domain_id=domain["id"])
print(retrieved)

if retrieved["records"] is not None:
    for record in retrieved["records"]:
        print(record)

update_params: resend.Domains.UpdateParams = {
    "id": domain["id"],
    "open_tracking": True,
    "click_tracking": True,
}

updated_domain: resend.Domains.UpdateResponse = resend.Domains.update(update_params)
print(f"Updated domain: {updated_domain['id']}")

domains: resend.Domains.ListResponse = resend.Domains.list()
if not domains:
    print("No domains found")
for d in domains["data"]:
    print(d)

verified_domain: resend.Domains.VerifyResponse = resend.Domains.verify(
    domain_id=domain["id"]
)
print(f"Verified")
print(verified_domain)

rm_domain: resend.Domains.RemoveResponse = resend.Domains.remove(domain_id=domain["id"])
print(rm_domain)
