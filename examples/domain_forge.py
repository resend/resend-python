import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

domain_id = "d91cd9bd-1176-453e-8fc1-35364d380206"

# Enable: activate Forge on an existing domain. Returns the full domain.
# Enabling an already-migrated domain is idempotent and returns its
# current state.
enable_params: resend.Domains.Forge.EnableParams = {
    "id": domain_id,
    "return_path": "send",
}
domain: resend.Domain = resend.Domains.Forge.enable(enable_params)
print(f"Forge enabled on domain: {domain['id']}")
print(f"Domain status: {domain['status']}")

# Update: move the return path and re-verify. After the domain verifies,
# the API refuses this with a 422 return_path_unavailable.
update_params: resend.Domains.Forge.UpdateParams = {
    "id": domain_id,
    "return_path": "outbound",
}
domain = resend.Domains.Forge.update(update_params)
print(f"Domain status after return path move: {domain['status']}")

# Verify: trigger asynchronous Forge verification, then poll Domains.get
# for the domain's state.
verified: resend.ForgeVerifyResponse = resend.Domains.Forge.verify(
    domain_id=domain_id
)
print(f"Verification triggered for domain: {verified['id']}")
