import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


resend.api_key = os.environ["RESEND_API_KEY"]

email = resend.Emails.send(
    sender="from@recomendo.io",
    to=["carlosderich@gmail.com"],
    subject="hi",
    html="<strong>hello, world!</strong>",
    reply_to="carlosderich@gmail.com",
    bcc="carlosderich@gmail.com",
    cc=["carlosderich@gmail.com"],
    tags=[
        {"name": "tag1", "value": "tagvalue1"},
        {"name": "tag2", "value": "tagvalue2"},
    ],
)
print(email)

email_resp = resend.Emails.get(email_id=email["id"])
print(email_resp)
