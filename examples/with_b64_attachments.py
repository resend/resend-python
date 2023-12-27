import base64
import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

f = open(
    os.path.join(os.path.dirname(__file__), "../resources/invoice.pdf"), "rb"
).read()

b64 = base64.b64encode(f)
b64_str = b64.decode("utf-8")

params = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hello with base64 attachments",
    "html": "<strong>hello, world!</strong>",
    "attachments": [{"filename": "invoice.pdf", "content": b64_str}],
}

email = resend.Emails.send(params)
print(email)
