import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

params: resend.Emails.SendParams = {
    "sender": "onboarding@resend.dev",
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

email = resend.Emails.send(params)
print(f"Email sent with id: {email.id}")

email_resp = resend.Emails.get(email_id=email.id)
print(f"Retrieved email: {email_resp.id}")
print(email_resp.__dict__)
