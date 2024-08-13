import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hi",
    "html": "<strong>hello, scheduled email!</strong>",
    "scheduled_at": "2024-09-05T11:52:01.858Z",
}

# Throws a resend.exceptions.ValidationError
# when scheduled_at is not in ISO 8601 format
email: resend.Email = resend.Emails.send(params)

print(f"Email scheduled")
print("Email ID: ", email["id"])

cancel_resp: resend.Emails.CancelScheduledEmailResponse = resend.Emails.cancel(
    email_id=email["id"]
)

print(f"Canceled email: {cancel_resp['id']}")
