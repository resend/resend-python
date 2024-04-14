import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


create_params: resend.Domains.CreateParams = {
    "name": "example.com",
    "region": "us-east-1",
}
domain = resend.Domains.create(params = create_params)
print(f'Crated domain {domain.name} with id {domain.id}')

retrieved = resend.Domains.get(domain_id=domain.id)
print(retrieved.__dict__)
for record in retrieved.records:
    print(record.__dict__)

update_params: resend.Domains.UpdateParams = {
    "id": domain.id,
    "open_tracking": True,
    "click_tracking": True,
}

updated_domain = resend.Domains.update(update_params)
print(f'Updated domain: {updated_domain.id}')

domains = resend.Domains.list()
if not domains:
    print("No domains found")
for domain in domains:
    print(domain.__dict__)

resend.Domains.verify(domain_id=domain.id)
print("domain verified")

domain = resend.Domains.remove(domain_id=domain.id)
print(f"domain id: {domain.id} deleted: {domain.deleted}")

domain = resend.Domains.verify(domain_id=domain.id)
print(f'Verified domain: {domain.id}')
print(domain.id)