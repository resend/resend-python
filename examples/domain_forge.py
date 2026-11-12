import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

domain_id = "d91cd9bd-1176-453e-8fc1-35364d380206"

# Enable: activate Forge on an existing domain. Returns the full domain.
# return_path is optional: when omitted, Resend picks a free DNS label.
# Enabling an already-migrated domain is idempotent and returns its
# current state.
enable_params: resend.Domains.Forge.EnableParams = {
    "id": domain_id,
    "return_path": "send",
}
domain: resend.Domain = resend.Domains.Forge.enable(enable_params)
print(f"Forge enabled on domain: {domain['id']}")
print(f"Domain status: {domain['status']}")

# Move the Forge return path with the classic domain update. This does not
# start verification: fetch the new record with Domains.get, add it to your
# DNS, then verify with scope=["forge"].
update_params: resend.Domains.UpdateParams = {
    "id": domain_id,
    "forge_return_path": "outbound",
}
updated = resend.Domains.update(update_params)
print(f"Forge return path moved on domain: {updated['id']}")

# Verify only the Forge record with the classic domain verify, scoped to
# Forge. Verification runs asynchronously; poll Domains.get for the state.
verify_params: resend.Domains.VerifyParams = {"scope": ["forge"]}
verified = resend.Domains.verify(domain_id=domain_id, params=verify_params)
print(f"Forge verification triggered for domain: {verified['id']}")
