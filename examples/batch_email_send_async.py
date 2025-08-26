import asyncio
import os
from typing import List

import resend
import resend.exceptions

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client
resend.default_http_client = resend.HTTPXClient()


async def main() -> None:
    params: List[resend.Emails.SendParams] = [
        {
            "from": "onboarding@resend.dev",
            "to": ["delivered@resend.dev"],
            "subject": "hey",
            "html": "<strong>hello, world!</strong>",
        },
        {
            "from": "onboarding@resend.dev",
            "to": ["delivered@resend.dev"],
            "subject": "hello",
            "html": "<strong>hello, world!</strong>",
        },
    ]

    try:
        # Send batch emails
        print("sending without idempotency_key")
        emails: resend.Batch.SendResponse = await resend.Batch.send_async(params)
        for email in emails["data"]:
            print(f"Email id: {email['id']}")
    except resend.exceptions.ResendError as err:
        print("Failed to send batch emails")
        print(f"Error: {err}")
        exit(1)

    try:
        # Send batch emails with idempotency_key
        print("sending with idempotency_key")

        options: resend.Batch.SendOptions = {
            "idempotency_key": "af477dc78aa9fa91fff3b8c0d4a2e1a5",
        }

        e: resend.Batch.SendResponse = await resend.Batch.send_async(
            params, options=options
        )
        for email in e["data"]:
            print(f"Email id: {email['id']}")
    except resend.exceptions.ResendError as err:
        print("Failed to send batch emails")
        print(f"Error: {err}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
