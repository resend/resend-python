import base64
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Read file
f = open(
    os.path.join(os.path.dirname(__file__), "../resources/invoice.pdf"), "rb"
).read()

# Read file bytes as a base64 string
b64: bytes = base64.b64encode(f)
b64_str: str = b64.decode("utf-8")

# Create attachment object from base64 string
b64_attachment: resend.Attachment = {"filename": "invoice.pdf", "content": b64_str}

# Email params
params: resend.Emails.SendParams = {
    "from_": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hello with base64 attachments",
    "html": "<strong>hello, world!</strong>",
    "attachments": [b64_attachment],
}

# Send email
email: resend.Email = resend.Emails.send(params)
print("Email sent with base64 string attachment")
print(f"Email ID: {email.id}")
