import os
from typing import List

import resend
import resend.exceptions

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


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
    emails: resend.Batch.SendResponse = resend.Batch.send(params)
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

    e: resend.Batch.SendResponse = resend.Batch.send(params, options=options)
    for email in e["data"]:
        print(f"Email id: {email['id']}")
except resend.exceptions.ResendError as err:
    print("Failed to send batch emails")
    print(f"Error: {err}")
    exit(1)

try:
    # Send batch emails with permissive validation mode
    print("sending with permissive validation mode")

    # Example with some invalid emails to demonstrate error handling
    mixed_params: List[resend.Emails.SendParams] = [
        {
            "from": "onboarding@resend.dev",
            "to": ["delivered@resend.dev"],
            "subject": "Valid email",
            "html": "<strong>This should work!</strong>",
        },
        {
            "from": "onboarding@resend.dev",
            "to": [],  # Invalid - empty to field
            "subject": "Invalid email",
            "html": "<strong>This should fail!</strong>",
        },
    ]

    options_permissive: resend.Batch.SendOptions = {
        "batch_validation": "permissive",
    }

    result: resend.Batch.SendResponse = resend.Batch.send(
        mixed_params, options=options_permissive
    )

    print(f"Successfully sent {len(result['data'])} emails:")
    for email in result["data"]:
        print(f"  Email id: {email['id']}")

    if "errors" in result and result["errors"]:
        print(f"Validation errors for {len(result['errors'])} emails:")
        for error in result["errors"]:
            print(f"  Index {error['index']}: {error['message']}")

except resend.exceptions.ResendError as err:
    print("Failed to send batch emails")
    print(f"Error: {err}")
    exit(1)
