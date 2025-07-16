import asyncio
import os
from typing import List

import resend
import resend.broadcasts

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client
resend.default_http_client = resend.HTTPXClient()

# replace with some existing audience id
audience_id: str = "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e"


async def main() -> None:
    create_params: resend.Broadcasts.CreateParams = {
        "audience_id": audience_id,
        "from": "onboarding@resend.dev",
        "subject": "Hello, world! (Async)",
        "html": "<p>Hello, world!</p>",
        "text": "Hello, world!",
        "reply_to": ["foo@resend.dev", "bar@resend.dev"],
        "name": "Hello, world! (Async)",
    }

    broadcast: resend.Broadcasts.CreateResponse = await resend.Broadcasts.create_async(
        create_params
    )
    print("Created broadcast !")
    print(broadcast)

    update_params: resend.Broadcasts.UpdateParams = {
        "broadcast_id": broadcast["id"],
        "html": "<p>Hello, world! Updated (Async)</p>",
        "text": "Hello, world! Updated (Async)",
        "name": "Hello, world! Updated (Async)",
    }

    updated_broadcast: resend.Broadcasts.UpdateResponse = (
        await resend.Broadcasts.update_async(update_params)
    )
    print("Updated broadcast!")
    print(updated_broadcast)

    send_params: resend.Broadcasts.SendParams = {
        "broadcast_id": broadcast["id"],
    }
    sent: resend.Broadcasts.SendResponse = await resend.Broadcasts.send_async(
        send_params
    )
    print("Sent broadcast !\n")
    print(sent)

    retrieved: resend.Broadcast = await resend.Broadcasts.get_async(id=broadcast["id"])
    print("retrieved broadcast !\n")
    print(retrieved)

    if retrieved["status"] == "draft":
        removed: resend.Broadcasts.RemoveResponse = (
            await resend.Broadcasts.remove_async(id=broadcast["id"])
        )
        print("Removed broadcast !\n")
        print(removed)
        print("\n")
    else:
        print("Broadcast is not in draft status, cannot remove it.\n")

    list_response: resend.Broadcasts.ListResponse = await resend.Broadcasts.list_async()
    print("List of broadcasts !\n")
    print(list_response)


if __name__ == "__main__":
    asyncio.run(main())
