import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

grants: resend.OAuthGrants.ListResponse = resend.OAuthGrants.list()
print(f"Found {len(grants['data'])} OAuth grants")
print(f"Has more grants: {grants['has_more']}")
if not grants["data"]:
    print("No OAuth grants found")
for grant in grants["data"]:
    print(grant["id"])
    print(grant["client_id"])
    print(grant["scopes"])
    print(grant["created_at"])
    print(grant["client"]["name"])

print("\n--- Using pagination parameters ---")
if grants["data"]:
    paginated_params: resend.OAuthGrants.ListParams = {
        "limit": 5,
        "after": grants["data"][0]["id"],
    }
    paginated_grants: resend.OAuthGrants.ListResponse = resend.OAuthGrants.list(
        params=paginated_params
    )
    print(f"Retrieved {len(paginated_grants['data'])} grants with pagination")
    print(f"Has more grants: {paginated_grants['has_more']}")
else:
    print("No OAuth grants available for pagination example")

if grants["data"]:
    revoked: resend.OAuthGrants.RevokeOAuthGrantResponse = resend.OAuthGrants.revoke(
        oauth_grant_id=grants["data"][0]["id"]
    )
    print(f"Revoked OAuth grant: {revoked['id']}")
    print(f"Revoked at: {revoked['revoked_at']}")
    print(f"Revoked reason: {revoked['revoked_reason']}")
