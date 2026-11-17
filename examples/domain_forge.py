import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

domain_id = os.environ.get("RESEND_DOMAIN_ID")
if not domain_id:
    raise EnvironmentError("RESEND_DOMAIN_ID is missing")

# Enable: activate Forge on an existing domain. Returns the full domain.
# custom_return_path is optional: when omitted, Resend picks a free DNS label.
# It is set once and cannot be changed afterwards. Enabling an
# already-migrated domain is idempotent and returns its current state.
enable_params: resend.Domains.Forge.EnableParams = {
    "id": domain_id,
    "custom_return_path": "send",
}
domain: resend.Domain = resend.Domains.Forge.enable(enable_params)
print(f"Forge enabled on domain: {domain['id']}")
print(f"Domain status: {domain['status']}")

# Verify only the Forge record with the classic domain verify, scoped to
# Forge. Verification runs asynchronously; poll Domains.get for the state.
verify_params: resend.Domains.VerifyParams = {"scope": ["forge"]}
verified = resend.Domains.verify(domain_id=domain_id, params=verify_params)
print(f"Forge verification triggered for domain: {verified['id']}")
