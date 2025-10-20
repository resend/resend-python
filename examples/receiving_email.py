import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Retrieve a single received email by ID
email_id = "006e2796-ff6a-4436-91ad-0429e600bf8a"

received_email: resend.ReceivedEmail = resend.Emails.Receiving.get(email_id=email_id)

print(f"\nRetrieved received email: {received_email['id']}")
print("\n--- Email Details ---")
print(f"From: {received_email['from']}")
print(f"To: {received_email['to']}")
print(f"Subject: {received_email['subject']}")
print(f"Created at: {received_email['created_at']}")
print(f"Object type: {received_email['object']}")

print("\n--- Email Content ---")
if received_email.get("html"):
    print(f"HTML: {received_email['html'][:100]}...")  # Show first 100 chars
else:
    print("HTML: None")

if received_email.get("text"):
    print(f"Text: {received_email['text'][:100]}...")  # Show first 100 chars
else:
    print("Text: None")

print("\n--- Recipients ---")
print(f"CC: {received_email.get('cc', [])}")
print(f"BCC: {received_email.get('bcc', [])}")
print(f"Reply-To: {received_email.get('reply_to', [])}")

print("\n--- Headers ---")
if received_email.get("headers"):
    for header_name, header_value in received_email["headers"].items():
        print(f"{header_name}: {header_value}")
else:
    print("No custom headers")

print("\n--- Attachments ---")
if received_email["attachments"]:
    print(f"Total attachments: {len(received_email['attachments'])}")
    for idx, attachment in enumerate(received_email["attachments"], 1):
        print(f"\nAttachment {idx}:")
        print(f"  ID: {attachment['id']}")
        print(f"  Filename: {attachment['filename']}")
        print(f"  Content Type: {attachment['content_type']}")
        print(f"  Content Disposition: {attachment['content_disposition']}")
        if attachment.get("content_id"):
            print(f"  Content ID: {attachment['content_id']}")
        if attachment.get("size"):
            print(f"  Size: {attachment['size']} bytes")
else:
    print("No attachments")

# List all received emails
print("\n--- Listing All Received Emails ---")
all_emails: resend.Emails.Receiving.ListResponse = resend.Emails.Receiving.list()

print(f"Total emails in this batch: {len(all_emails['data'])}")
print(f"Has more emails: {all_emails['has_more']}")

if all_emails["data"]:
    for idx, email in enumerate(all_emails["data"], 1):
        print(f"\nEmail {idx}:")
        print(f"  ID: {email['id']}")
        print(f"  From: {email['from']}")
        print(f"  To: {email['to']}")
        print(f"  Subject: {email['subject']}")
        print(f"  Created: {email['created_at']}")
        print(f"  Attachments: {len(email['attachments'])}")

# List with pagination
print("\n--- Listing Received Emails with Pagination ---")
list_params: resend.Emails.Receiving.ListParams = {
    "limit": 5,
}
paginated_emails: resend.Emails.Receiving.ListResponse = resend.Emails.Receiving.list(
    params=list_params
)

print(f"Retrieved {len(paginated_emails['data'])} emails (limited to 5)")
print(f"Has more: {paginated_emails['has_more']}")

# Example with cursor-based pagination
if paginated_emails["data"] and paginated_emails["has_more"]:
    last_email_id = paginated_emails["data"][-1]["id"]
    print(f"\n--- Getting Next Page (after {last_email_id}) ---")
    next_page_params: resend.Emails.Receiving.ListParams = {
        "limit": 5,
        "after": last_email_id,
    }
    next_page: resend.Emails.Receiving.ListResponse = resend.Emails.Receiving.list(
        params=next_page_params
    )
    print(f"Next page has {len(next_page['data'])} emails")
    print(f"Next page has more: {next_page['has_more']}")

print("\n" + "=" * 60)
print("ATTACHMENTS EXAMPLES")
print("=" * 60)

# List all attachments for a received email
print("\n--- Listing All Attachments ---")
list_attachments_params: resend.Attachments.Receiving.ListParams = {
    "email_id": email_id,
}
all_attachments: resend.Attachments.Receiving.ListResponse = (
    resend.Attachments.Receiving.list(params=list_attachments_params)
)

print(f"Total attachments: {len(all_attachments['data'])}")
print(f"Has more: {all_attachments['has_more']}")

if all_attachments["data"]:
    for idx, att in enumerate(all_attachments["data"], 1):
        print(f"\nAttachment {idx}:")
        print(f"  ID: {att['id']}")
        print(f"  Filename: {att['filename']}")
        print(f"  Content Type: {att['content_type']}")
        print(f"  Size: {att.get('size', 'N/A')} bytes")

# Retrieve a specific attachment from a received email
if received_email["attachments"] and len(received_email["attachments"]) > 0:
    first_attachment = received_email["attachments"][0]
    attachment_id = first_attachment["id"]

    print(f"\n--- Retrieving Attachment Details: {first_attachment['filename']} ---")

    attachment_details: resend.ReceivedEmailAttachmentDetails = (
        resend.Attachments.Receiving.get(
            email_id=email_id,
            attachment_id=attachment_id,
        )
    )

    print(f"Attachment ID: {attachment_details['id']}")
    print(f"Filename: {attachment_details['filename']}")
    print(f"Content Type: {attachment_details['content_type']}")
    print(f"Content Disposition: {attachment_details['content_disposition']}")
    if attachment_details.get("content_id"):
        print(f"  Content ID: {attachment_details['content_id']}")
    print(f"Download URL: {attachment_details['download_url']}")
    print(f"Expires At: {attachment_details['expires_at']}")
else:
    print("\nNo attachments available to retrieve in this example.")
