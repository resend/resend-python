"""
Example demonstrating how to access response headers.

Response headers include useful information like rate limits, request IDs, etc.
"""

import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "Hello from Resend",
    "html": "<strong>Hello, world!</strong>",
}

resp: resend.Emails.SendResponse = resend.Emails.send(params)
print(f"Email sent! ID: {resp['id']}")

if "headers" in resp:
    print(f"Request ID: {resp['headers'].get('x-request-id')}")
    print(f"Rate limit: {resp['headers'].get('x-ratelimit-limit')}")
    print(f"Rate limit remaining: {resp['headers'].get('x-ratelimit-remaining')}")
    print(f"Rate limit reset: {resp['headers'].get('x-ratelimit-reset')}")

print("\n")
print("Example 3: Rate limit tracking")


def send_with_rate_limit_check(params: resend.Emails.SendParams) -> str:
    """Example function showing how to track rate limits."""
    response = resend.Emails.send(params)

    # Access headers via dict key
    headers = response.get("headers", {})
    remaining = headers.get("x-ratelimit-remaining")
    limit = headers.get("x-ratelimit-limit")

    if remaining and limit:
        print(f"Rate limit usage: {int(limit) - int(remaining)}/{limit}")
        if int(remaining) < 10:
            print("Warning: Approaching rate limit!")

    return response["id"]


email_id = send_with_rate_limit_check(params)
print(f"Sent email with ID: {email_id}")
