import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

print("Step 1: Creating template variables...")
variables: List[resend.Variable] = [
    {
        "key": "NAME",
        "type": "string",
        "fallback_value": "user",
    },
    {
        "key": "AGE",
        "type": "number",
        "fallback_value": 25,
    },
]

print("Step 2: Creating a new template...")
create_params: resend.Templates.CreateParams = {
    "name": "user-welcome-template",
    "subject": "Welcome to our platform!",
    "html": """
    <html>
        <body>
            <h1>Welcome, {{{NAME}}}!</h1>
            <p>Thank you for joining us. Your age is {{{AGE}}}.</p>
        </body>
    </html>
    """,
    "variables": variables,
}

template: resend.Templates.CreateResponse = resend.Templates.create(create_params)
print(f"Created template: {template['id']}")

print("Publishing the template...")
published: resend.Templates.PublishResponse = resend.Templates.publish(template["id"])
print(f"Published template: {published['id']}")

# Create the template configuration with variables
email_template: resend.EmailTemplate = {
    "id": template["id"],
    "variables": {
        "NAME": "John Doe",
        "AGE": 30,
    },
}

# Send the email with the template
send_params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": ["delivered@resend.dev"],
    "template": email_template,
}

email: resend.Emails.SendResponse = resend.Emails.send(send_params)
print(f"✓ Sent email using template: {email['id']}")

sent_email: resend.Email = resend.Emails.get(email["id"])
print(f"✓ Retrieved email: {sent_email['id']}")
print(f"  From: {sent_email['from']}")
print(f"  To: {sent_email['to']}")
print(f"  Subject: {sent_email.get('subject', 'N/A')}")

print("Cleaning up - removing the template...")
removed: resend.Templates.RemoveResponse = resend.Templates.remove(template["id"])
print(f"Deleted template: {removed['id']}, deleted={removed['deleted']}")
