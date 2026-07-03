import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


# Start a claim for a domain that another Resend account has already verified.
claim_params: resend.Domains.Claims.CreateParams = {
    "name": "example.com",
    "region": "us-east-1",
}
claim: resend.DomainClaim = resend.Domains.Claims.create(claim_params)
print(f"Created domain claim: {claim['id']}")
print(f"Status: {claim['status']}")
if claim.get("record"):
    record = claim["record"]
    print(
        f"Add this TXT record to prove ownership: {record['name']} = {record['value']}"
    )

# Get: poll the claim until the TXT record has been added and verification can run.
domain_id = claim["domain_id"]
if domain_id:
    retrieved_claim: resend.DomainClaim = resend.Domains.Claims.get(domain_id=domain_id)
    print(f"Retrieved domain claim status: {retrieved_claim['status']}")

    # Verify: trigger asynchronous DNS verification and ownership transfer.
    verified_claim: resend.DomainClaim = resend.Domains.Claims.verify(
        domain_id=domain_id
    )
    print(f"Verification triggered, claim status: {verified_claim['status']}")
