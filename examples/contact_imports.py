import os
import time

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

ts = int(time.time())
csv_path = os.path.join(os.path.dirname(__file__), "contacts.csv")
with open(csv_path, "rb") as f:
    file_content = f.read().replace(b"steve@example.com,Steve,Wozniak", f"steve+{ts}@example.com,Steve,Wozniak".encode())

create_params: resend.Contacts.Imports.CreateParams = {
    "file": file_content,
    "column_map": {
        "email": "Email",
        "first_name": "First Name",
        "last_name": "Last Name",
        "properties": {
            "plan": {
                "column": "Plan",
                "type": "string",
            },
        },
    },
    "on_conflict": "upsert",
    "segments": [{"id": "60a2ac5e-0774-456e-817d-ebf40f6dba31"}],
    "topics": [
        {
            "id": "6eb54030-9489-4e9c-8de6-cd337c5fef1e",
            "subscription": "opt_in",
        },
    ],
}

import_response: resend.Contacts.Imports.CreateContactImportResponse = (
    resend.Contacts.Imports.create(create_params)
)
print("Created contact import with ID: {}".format(import_response["id"]))
print(import_response)

contact_import: resend.ContactImport = resend.Contacts.Imports.get(import_response["id"])
print("Retrieved contact import")
print(contact_import)

list_response: resend.Contacts.Imports.ListContactImportsResponse = (
    resend.Contacts.Imports.list()
)
print(f"Found {len(list_response['data'])} imports")
print(f"Has more: {list_response['has_more']}")
for item in list_response["data"]:
    print(item)
