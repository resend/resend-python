import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

f: bytes = open(
    os.path.join(os.path.dirname(__file__), "../resources/resend-wordmark-black.png"),
    "rb",
).read()

# Define the file attachment
attachment: resend.Attachment = {
    "filename": "resend-wordmark-black.png",
    "content": list(f),
    "content_type": "image/png",
    # This is the content ID that will be used in the HTML to reference the image
    "inline_content_id": "my-test-image",
}

# Define the email parameters
params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "Inline attachment test from Resend's python SDK",
    "html": '<p>This is an email with an <img width=100 height=40 src="cid:my-test-image" /> embed image</p>',
    "attachments": [attachment],
}

email: resend.Email = resend.Emails.send(params)
print("Sent email with attachment")
print(email)
