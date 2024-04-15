import os
from typing import List
import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


params: List[resend.Emails.SendParams] = [
    {
        "sender": "onboarding@resend.dev",
        "to": ["carlosderich@gmail.com"],
        "subject": "hey",
        "html": "<strong>hello, world!</strong>",
    },
    {
        "sender": "onboarding@resend.dev",
        "to": ["carlosderich@gmail.com"],
        "subject": "hello",
        "html": "<strong>hello, world!</strong>",
    },
]

emails = resend.Batch.send(params)
for email in emails:
    print(f'Email sent with id: {email.id}')