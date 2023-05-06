import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


f = open(
    os.path.join(os.path.dirname(__file__), "../resources/invoice.pdf"), "rb"
).read()

params = {
    "from": "d@recomendo.io",
    "to": "to@gmail.com",
    "subject": "hi",
    "html": "<strong>hello, world!</strong>",
    "attachments": [{"filename": "invoice.pdf", "content": list(f)}],
}

r = resend.Emails.send(params)
print(r)
