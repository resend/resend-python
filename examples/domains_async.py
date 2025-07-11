import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client
resend.default_http_client = resend.HTTPXClient()


async def main() -> None:
    create_params: resend.Domains.CreateParams = {
        "name": "example.com",
        "region": "us-east-1",
        "custom_return_path": "outbound",
    }
    domain: resend.Domain = await resend.Domains.create_async(params=create_params)
    print(domain)

    retrieved: resend.Domain = await resend.Domains.get_async(domain_id=domain["id"])
    if retrieved["records"] is not None:
        for record in retrieved["records"]:
            print(record)

    update_params: resend.Domains.UpdateParams = {
        "id": domain["id"],
        "open_tracking": True,
        "click_tracking": True,
        "tls": "enforced",
    }

    updated_domain: resend.Domain = await resend.Domains.update_async(update_params)
    print(f"Updated domain: {updated_domain['id']}")

    domains: resend.Domains.ListResponse = await resend.Domains.list_async()
    if not domains:
        print("No domains found")
    for domain in domains["data"]:
        print(domain)

    verified_domain: resend.Domain = await resend.Domains.verify_async(
        domain_id=domain["id"]
    )
    print(f"Verified")
    print(verified_domain)

    rm_domain: resend.Domain = await resend.Domains.remove_async(domain_id=domain["id"])
    print(rm_domain)


if __name__ == "__main__":
    asyncio.run(main())
