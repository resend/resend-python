import asyncio
import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client
resend.default_http_client = resend.HTTPXClient()


async def main() -> None:
    create_params: resend.Audiences.CreateParams = {
        "name": "New Audience from Python SDK (Async)",
    }
    audience: resend.Audience = await resend.Audiences.create_async(create_params)
    print(f"Created audience: {audience['id']}")
    print(audience)

    aud: resend.Audience = await resend.Audiences.get_async(audience["id"])
    print("Retrieved audience: ", aud)

    audiences: resend.Audiences.ListResponse = await resend.Audiences.list_async()
    print("List of audiences:", [a["id"] for a in audiences["data"]])

    rmed: resend.Audience = await resend.Audiences.remove_async(id=audience["id"])
    print(f"Deleted audience")
    print(rmed)


if __name__ == "__main__":
    asyncio.run(main())
