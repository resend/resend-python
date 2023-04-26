import os

from resend import Resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

client = Resend(api_key=os.environ["RESEND_API_KEY"])

f = open(
    os.path.join(os.path.dirname(__file__), "../resources/invoice.pdf"), "rb"
).read()

r = client.send_email(
    sender="from@example.io",
    to="to@email.com",
    subject="hi",
    html="<strong>hello, world!</strong>",
    attachments=[{"filename": "invoice.pdf", "content": list(f)}],
)
print(r)
