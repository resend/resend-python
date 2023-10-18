import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


params = [
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

emails = resend.Batch.send(params)
print(emails)