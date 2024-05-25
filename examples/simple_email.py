import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
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

email: resend.Email = resend.Emails.send(params)
print(f"Sent email")
print("Email ID: ", email["id"])

email_resp: resend.Email = resend.Emails.get(email_id=email["id"])
print(f"Retrieved email: {email_resp['id']}")
print("Email ID: ", email_resp["id"])
print("Email from: ", email_resp["from"])
print("Email to: ", email_resp["to"])
print("Email subject: ", email_resp["subject"])
print("Email html: ", email_resp["html"])
print("Email created_at: ", email_resp["created_at"])
print("Email reply_to: ", email_resp["reply_to"])
print("Email bcc: ", email_resp["bcc"])
print("Email cc: ", email_resp["cc"])
