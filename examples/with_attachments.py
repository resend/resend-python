import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


# Read file
f: bytes = open(
    os.path.join(os.path.dirname(__file__), "../resources/invoice.pdf"), "rb"
).read()

# Define the file attachment
attachment: resend.Attachment = {"filename": "invoice.pdf", "content": list(f)}

# Define the email parameters
params: resend.Emails.SendParams = {
    "sender": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hi",
    "html": "<strong>hello, world!</strong>",
    "attachments": [attachment],
}

r = resend.Emails.send(params)
print("Sent email with attachment")
print(f"Email ID: {r.id}")
