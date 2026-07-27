import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


async def main() -> None:
    add_params: resend.Suppressions.AddParams = {
        "email": "blocked@example.com",
    }
    added = await resend.Suppressions.add_async(add_params)
    print(f"Added suppression: {added['id']}")

    list_params: resend.Suppressions.ListParams = {
        "origin": "bounce",
        "limit": 10,
    }
    suppressions = await resend.Suppressions.list_async(list_params)
    print(f"Has more: {suppressions['has_more']}")
    for suppression in suppressions["data"]:
        print(f"{suppression['email']} ({suppression['origin']})")

    found: resend.Suppression = await resend.Suppressions.get_async(
        "blocked@example.com"
    )
    print(f"Suppressed at: {found['created_at']}")

    batch_add_params: resend.Suppressions.Batch.AddParams = {
        "emails": ["one@example.com", "two@example.com"],
    }
    batch_added = await resend.Suppressions.Batch.add_async(batch_add_params)
    print(f"Batch added {len(batch_added['data'])} suppressions")

    batch_remove_params: resend.Suppressions.Batch.RemoveParams = {
        "ids": [entry["id"] for entry in batch_added["data"]],
    }
    batch_removed = await resend.Suppressions.Batch.remove_async(batch_remove_params)
    print(f"Batch removed {len(batch_removed['data'])} suppressions")

    removed = await resend.Suppressions.remove_async("blocked@example.com")
    print(f"Removed suppression {removed['id']}: deleted={removed['deleted']}")


if __name__ == "__main__":
    asyncio.run(main())
