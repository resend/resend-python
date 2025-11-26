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

print("=" * 60)
print("Example 1: Without type annotations")
print("=" * 60)

response = resend.Emails.send(params)
print(f"Email sent! ID: {response['id']}")
print(f"Request ID: {response['headers'].get('x-request-id')}")
print(f"Rate limit: {response['headers'].get('x-ratelimit-limit')}")
print(f"Rate limit remaining: {response['headers'].get('x-ratelimit-remaining')}")
print(f"Rate limit reset: {response['headers'].get('x-ratelimit-reset')}")

print("\n" + "=" * 60)
print("Example 2: With type annotations")
print("=" * 60)

typed_response: resend.Emails.SendResponse = resend.Emails.send(params)
print(f"Email sent! ID: {typed_response['id']}")

if "headers" in typed_response:
    print(f"Request ID: {typed_response['headers'].get('x-request-id')}")
    print(f"Rate limit: {typed_response['headers'].get('x-ratelimit-limit')}")
    print(
        f"Rate limit remaining: {typed_response['headers'].get('x-ratelimit-remaining')}"
    )
    print(f"Rate limit reset: {typed_response['headers'].get('x-ratelimit-reset')}")

print("\n" + "=" * 60)
print("Example 3: Rate limit tracking")
print("=" * 60)


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
            print("⚠️  Warning: Approaching rate limit!")

    return response["id"]


email_id = send_with_rate_limit_check(params)
print(f"Sent email with ID: {email_id}")
