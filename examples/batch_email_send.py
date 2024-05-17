import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


params: List[resend.Emails.SendParams] = [
    {
        "sender": "carlosderich@gmail.com",
        "to": ["delivered@resend.dev"],
        "subject": "hey",
        "html": "<strong>hello, world!</strong>",
    },
    {
        "sender": "carlosderich@gmail.com",
        "to": ["delivered@resend.dev"],
        "subject": "hello",
        "html": "<strong>hello, world!</strong>",
    },
]

emails = resend.Batch.send(params)
for email in emails:
    print(f"Email sent with id: {email.id}")
