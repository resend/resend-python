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
    emails: resend.Batch.BatchEmails = resend.Batch.send(params)
except resend.exceptions.ResendError as e:
    print("Failed to send batch emails")
    print(f"Error: {e}")
    exit(1)

for email in emails["data"]:
    print(f"Email sent with id: {email["id"]}")
