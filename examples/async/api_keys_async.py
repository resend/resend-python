import asyncio
import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client


async def main() -> None:
    create_params: resend.ApiKeys.CreateParams = {
        "name": "example.com",
    }

    key = await resend.ApiKeys.create_async(params=create_params)
    print("Created new api key")
    print(f"Key id: {key['id']} and token: {key['token']}")

    update_params: resend.ApiKeys.UpdateParams = {
        "id": key["id"],
        "name": "renamed-example",
    }
    updated_key = await resend.ApiKeys.update_async(update_params)
    print(f"Updated api key: {updated_key['id']}")

    keys: resend.ApiKeys.ListResponse = await resend.ApiKeys.list_async()
    for k in keys["data"]:
        print(k["id"])
        print(k["name"])
        print(k["created_at"])

    if len(keys["data"]) > 0:
        await resend.ApiKeys.remove_async(api_key_id=keys["data"][0]["id"])
        print(f"Removed api key: {keys['data'][0]['id']}")


if __name__ == "__main__":
    asyncio.run(main())
