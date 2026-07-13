import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


async def main() -> None:
    grants: resend.OAuthGrants.ListResponse = await resend.OAuthGrants.list_async()
    print(f"Found {len(grants['data'])} OAuth grants")
    for grant in grants["data"]:
        print(grant["id"])
        print(grant["client_id"])
        print(grant["scopes"])
        print(grant["created_at"])
        print(grant["client"]["name"])

    if grants["data"]:
        revoked = await resend.OAuthGrants.revoke_async(
            oauth_grant_id=grants["data"][0]["id"]
        )
        print(f"Revoked OAuth grant: {revoked['id']}")
        print(f"Revoked at: {revoked['revoked_at']}")
        print(f"Revoked reason: {revoked['revoked_reason']}")


if __name__ == "__main__":
    asyncio.run(main())
