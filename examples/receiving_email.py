import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Retrieve a single received email by ID
email_id = "006e2796-ff6a-4436-91ad-0429e600bf8a"

received_email: resend.ReceivedEmail = resend.Emails.Receiving.get(
    email_id=email_id
)

print(f"Retrieved received email: {received_email['id']}")
print("\n--- Email Details ---")
print(f"From: {received_email['from']}")
print(f"To: {received_email['to']}")
print(f"Subject: {received_email['subject']}")
print(f"Created at: {received_email['created_at']}")
print(f"Object type: {received_email['object']}")

print("\n--- Email Content ---")
if received_email.get('html'):
    print(f"HTML: {received_email['html'][:100]}...")  # Show first 100 chars
else:
    print("HTML: None")

if received_email.get('text'):
    print(f"Text: {received_email['text'][:100]}...")  # Show first 100 chars
else:
    print("Text: None")

print("\n--- Recipients ---")
print(f"CC: {received_email.get('cc', [])}")
print(f"BCC: {received_email.get('bcc', [])}")
print(f"Reply-To: {received_email.get('reply_to', [])}")

print("\n--- Headers ---")
if received_email.get('headers'):
    for header_name, header_value in received_email['headers'].items():
        print(f"{header_name}: {header_value}")
else:
    print("No custom headers")

print("\n--- Attachments ---")
if received_email['attachments']:
    print(f"Total attachments: {len(received_email['attachments'])}")
    for idx, attachment in enumerate(received_email['attachments'], 1):
        print(f"\nAttachment {idx}:")
        print(f"  ID: {attachment['id']}")
        print(f"  Filename: {attachment['filename']}")
        print(f"  Content Type: {attachment['content_type']}")
        print(f"  Content Disposition: {attachment['content_disposition']}")
        if attachment.get('content_id'):
            print(f"  Content ID: {attachment['content_id']}")
else:
    print("No attachments")
