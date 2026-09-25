import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


async def main() -> None:
    usage: resend.Usage.GetResponse = await resend.Usage.get_async()

    print(f"Daily emails used: {usage['emails']['daily']['used']}")
    print(f"Monthly emails used: {usage['emails']['monthly']['used']}")
    print(f"Contacts used: {usage['contacts']['used']}")
    print(f"Rate limit: {usage['rate_limit']['limit']} per {usage['rate_limit']['duration']}")


if __name__ == "__main__":
    asyncio.run(main())
