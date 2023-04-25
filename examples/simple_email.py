import os

from resend import Resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

client = Resend(api_key=os.environ["RESEND_API_KEY"])

r = client.send_email(
    sender="team@recomendo.io",
    to="carlosderich@gmail.com",
    subject="hi",
    html="<strong>hello, world!</strong>",
)
print(r)
