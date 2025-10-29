import os

import resend
# Type imports
from resend import EmailAttachments

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


# Read file
f: bytes = open(
    os.path.join(os.path.dirname(__file__), "../resources/invoice.pdf"), "rb"
).read()

# Define the file attachment
attachment: resend.Attachment = {
    "filename": "invoice.pdf",
    "content": list(f),
    "content_type": "application/pdf",
}

# Define the email parameters
params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "subject": "hi",
    "html": "<strong>hello, world!</strong>",
    "attachments": [attachment],
}

email: resend.Emails.SendResponse = resend.Emails.send(params)
print("Sent email with attachment")
print(email)

print("\n--- Retrieving Attachments ---")

# List all attachments from the sent email
attachments = resend.Emails.Attachments.list(email_id=email["id"])
print(f"Email has {len(attachments['data'])} attachment(s)")
print(f"Has more attachments: {attachments['has_more']}")

# Get details of each attachment
if attachments["data"]:
    for i, attachment_item in enumerate(attachments["data"], 1):
        print(f"\nAttachment {i}: {attachment_item['filename']}")
        print(f"  - ID: {attachment_item['id']}")
        print(f"  - Content Type: {attachment_item['content_type']}")
        print(f"  - Size: {attachment_item['size']} bytes")
        print(
            f"  - Content Disposition: {attachment_item.get('content_disposition', 'N/A')}"
        )

        # Get detailed information about this attachment (including download URL)
        attachment_details = resend.Emails.Attachments.get(
            email_id=email["id"], attachment_id=attachment_item["id"]
        )
        print(f"  - Download URL: {attachment_details['download_url']}")
        print(f"  - Expires at: {attachment_details['expires_at']}")

# Example with pagination for attachments (useful when emails have many attachments)
print("\n--- Paginating Attachments ---")
attachment_params: EmailAttachments.ListParams = {
    "limit": 10,
}
paginated_attachments = resend.Emails.Attachments.list(
    email_id=email["id"], params=attachment_params
)
print(f"Retrieved {len(paginated_attachments['data'])} attachment(s) (limited to 10)")
