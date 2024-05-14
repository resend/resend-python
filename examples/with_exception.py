import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

params: resend.Emails.SendParams = {
    "sender": "onboarding@resend.dev",
    "to": ["invalid"],
    "subject": "hi",
    "html": "<strong>hello, world!</strong>",
}

try:
    email: resend.Email = resend.Emails.send(params)
except resend.exceptions.ResendError as e:
    print(f"Error sending email: {e}")
