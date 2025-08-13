import asyncio
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Set up async HTTP client
resend.default_http_client = resend.HTTPXClient()

params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hi",
    "html": "<strong>hello, world!</strong>",
    "reply_to": "to@gmail.com",
    "bcc": "delivered@resend.dev",
    "cc": ["delivered@resend.dev"],
    "tags": [
        {"name": "tag1", "value": "tagvalue1"},
        {"name": "tag2", "value": "tagvalue2"},
    ],
}


async def main() -> None:
    # Without Idempotency Key
    email_non_idempotent: resend.Email = await resend.Emails.send_async(params)
    print(f"Sent email without idempotency key: {email_non_idempotent['id']}")

    # With Idempotency Key
    options: resend.Emails.SendOptions = {
        "idempotency_key": "44",
    }
    email_idempotent: resend.Email = await resend.Emails.send_async(params, options)
    print(f"Sent email with idempotency key: {email_idempotent['id']}")

    email_resp: resend.Email = await resend.Emails.get_async(
        email_id=email_non_idempotent["id"]
    )
    print(f"Retrieved email: {email_resp['id']}")
    print("Email ID: ", email_resp["id"])
    print("Email from: ", email_resp["from"])
    print("Email to: ", email_resp["to"])
    print("Email subject: ", email_resp["subject"])
    print("Email html: ", email_resp["html"])
    print("Email created_at: ", email_resp["created_at"])
    print("Email reply_to: ", email_resp["reply_to"])
    print("Email bcc: ", email_resp["bcc"])
    print("Email cc: ", email_resp["cc"])


if __name__ == "__main__":
    asyncio.run(main())
