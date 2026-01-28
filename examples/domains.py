import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Domains.CreateParams = {
    "name": "example.com",
    "region": "us-east-1",
    "custom_return_path": "outbound",
}
domain: resend.Domains.CreateDomainResponse = resend.Domains.create(
    params=create_params
)
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
print(f"Found {len(domains['data'])} domains")
print(f"Has more domains: {domains['has_more']}")
if not domains["data"]:
    print("No domains found")
for listed_domain in domains["data"]:
    print(listed_domain)

print("\n--- Using pagination parameters ---")
if domains["data"]:
    paginated_params: resend.Domains.ListParams = {
        "limit": 2,
        "after": domains["data"][0]["id"],
    }
    paginated_domains: resend.Domains.ListResponse = resend.Domains.list(
        params=paginated_params
    )
    print(f"Retrieved {len(paginated_domains['data'])} domains with pagination")
    print(f"Has more domains: {paginated_domains['has_more']}")
else:
    print("No domains available for pagination example")

verified_domain: resend.Domain = resend.Domains.verify(domain_id=domain["id"])
print(f"Verified")
print(verified_domain)

rm_domain: resend.Domain = resend.Domains.remove(domain_id=domain["id"])
print(rm_domain)
