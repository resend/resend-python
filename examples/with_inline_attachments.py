import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

f: bytes = open(
    os.path.join(os.path.dirname(__file__), "../resources/resend-wordmark-black.png"),
    "rb",
).read()

# Send email with local inline attachment
local_attachment: resend.Attachment = {
    "filename": "resend-wordmark-black.png",
    "content": list(f),
    "content_type": "image/png",
    # This is the content ID that will be used in the HTML to reference the image
    "inline_content_id": "my-test-image",
}

local_params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "Local inline attachment test from Resend's python SDK",
    "html": '<p>This email contains a local inline attachment: <img width=100 height=40 src="cid:my-test-image" /></p>',
    "attachments": [local_attachment],
}

local_email: resend.Email = resend.Emails.send(local_params)
print("Sent email with local inline attachment")
print(local_email)

# Send email with remote inline attachment using content_id
remote_attachment: resend.RemoteAttachment = {
    "filename": "remote-resend-wordmark-black.png",
    "path": "https://resend.com/static/brand/resend-wordmark-black.png",
    "content_id": "my-test-image",  # Using content_id as alternative to inline_content_id
}

remote_params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "Remote inline attachment test from Resend's python SDK",
    "html": '<p>This email contains a remote inline attachment: <img width=100 height=40 src="cid:my-test-image" /></p>',
    "attachments": [remote_attachment],
}

remote_email: resend.Email = resend.Emails.send(remote_params)
print("Sent email with remote inline attachment")
print(remote_email)
