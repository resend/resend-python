import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Domains.CreateParams = {
    "name": "example.com",
    "region": "us-east-1",
}
domain: resend.Domain = resend.Domains.create(params=create_params)
print(f"Crated domain {domain.name} with id {domain.id}")

retrieved: resend.Domain = resend.Domains.get(domain_id=domain.id)
print(retrieved.__dict__)

if retrieved.records is not None:
    for record in retrieved.records:
        print(record.__dict__)

update_params: resend.Domains.UpdateParams = {
    "id": domain.id,
    "open_tracking": True,
    "click_tracking": True,
}

updated_domain: resend.Domain = resend.Domains.update(update_params)
print(f"Updated domain: {updated_domain.id}")

domains: List[resend.Domain] = resend.Domains.list()
if not domains:
    print("No domains found")
for domain in domains:
    print(domain.__dict__)

resend.Domains.verify(domain_id=domain.id)
print("domain verified")

rm_domain: resend.Domain = resend.Domains.remove(domain_id=domain.id)
print(f"domain id: {domain.id} deleted: {rm_domain.deleted}")

verified_domain: resend.Domain = resend.Domains.verify(domain_id=domain.id)
print(f"Verified domain: {verified_domain.id}")
