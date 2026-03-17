"""
Example demonstrating the three different types of headers in the Resend Python SDK:

1. Email headers (SendParams["headers"]): Custom MIME headers added to the outgoing
   email itself, visible to the recipient's mail client (e.g. X-Entity-Ref-ID).

2. HTTP response headers (response["http_headers"]): HTTP-level metadata returned
   by the Resend API, such as rate limit info and request IDs. These are injected
   by the SDK and are never part of the email content.

3. Inbound email MIME headers (email["headers"]): MIME headers present on a received
   email, returned as part of the API response body (e.g. X-Mailer, DKIM-Signature).
"""

import os

import resend

resend.api_key = os.environ["RESEND_API_KEY"]

# --- Example 1: Custom email headers (part of the outgoing email itself) ---

params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "Hello from Resend",
    "html": "<strong>Hello, world!</strong>",
    "headers": {
        "X-Entity-Ref-ID": "123456789",
    },
}

resp: resend.Emails.SendResponse = resend.Emails.send(params)
print(f"Email sent! ID: {resp['id']}")

# --- Example 2: HTTP response headers (SDK metadata, not part of the email) ---

if "http_headers" in resp:
    print(f"Rate limit: {resp['http_headers'].get('ratelimit-limit')}")
    print(f"Rate limit remaining: {resp['http_headers'].get('ratelimit-remaining')}")
    print(f"Rate limit reset: {resp['http_headers'].get('ratelimit-reset')}")

# --- Example 3: Inbound email MIME headers (from a received email response body) ---

# Replace with a real received email ID
received_email_id = os.environ.get("RECEIVED_EMAIL_ID", "")

if received_email_id:
    received: resend.ReceivedEmail = resend.Emails.Receiving.get(
        email_id=received_email_id
    )

    # email["headers"] — MIME headers of the inbound email, part of the API response body.
    # Completely separate from http_headers injected by the SDK.
    if received.get("headers"):
        print("Inbound email MIME headers:")
        for name, value in received["headers"].items():
            print(f"  {name}: {value}")

    # http_headers are also available on received email responses
    if received.get("http_headers"):
        print(f"Rate limit remaining: {received['http_headers'].get('ratelimit-remaining')}")
else:
    print("Set RECEIVED_EMAIL_ID env var to run the inbound email headers example.")

# --- Example 4: Rate limit tracking via HTTP response headers ---


def send_with_rate_limit_check(params: resend.Emails.SendParams) -> str:
    """Example function showing how to track rate limits."""
    response = resend.Emails.send(params)

    http_headers = response.get("http_headers", {})
    remaining = http_headers.get("ratelimit-remaining")
    limit = http_headers.get("ratelimit-limit")

    if remaining and limit:
        print(f"Rate limit usage: {int(limit) - int(remaining)}/{limit}")
        if int(remaining) < 10:
            print("Warning: Approaching rate limit!")

    return response["id"]


email_id = send_with_rate_limit_check(params)
print(f"Sent email with ID: {email_id}")
