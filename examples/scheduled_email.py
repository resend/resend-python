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
# when scheduled_at is not in ISO 8601 format.
#
# Here is an example on how to create a date in the ISO 8601 format:
# from datetime import datetime
# datetime.now().isoformat()
email: resend.Email = resend.Emails.send(params)

print(f"Email scheduled: {email['id']}")

update_params: resend.Emails.UpdateParams = {
    "id": email["id"],
    "scheduled_at": "2024-09-07T11:52:01.858Z",
}

updated_email: resend.Emails.UpdateEmailResponse = resend.Emails.update(
    params=update_params
)

print(f"Email updated: {updated_email['id']}")

cancel_resp: resend.Emails.CancelScheduledEmailResponse = resend.Emails.cancel(
    email_id=email["id"]
)

print(f"Email canceled: {cancel_resp['id']}")
