import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

csv_path = os.path.join(os.path.dirname(__file__), "contacts.csv")
with open(csv_path, "rb") as f:
    file_content = f.read()

create_params: resend.ContactImports.CreateParams = {
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
    "segments": ["60a2ac5e-0774-456e-817d-ebf40f6dba31"],
    "topics": [
        {
            "id": "059ac693-2fc8-4c13-8b27-01350d638a17",
            "subscription": "opt_in",
        },
    ],
}

import_response: resend.ContactImports.CreateContactImportResponse = (
    resend.Contacts.Imports.create(create_params)
)
print("Created contact import with ID: {}".format(import_response["id"]))
print(import_response)

contact_import: resend.ContactImport = resend.Contacts.Imports.get(import_response["id"])
print("Retrieved contact import")
print(contact_import)

list_response: resend.ContactImports.ListContactImportsResponse = (
    resend.Contacts.Imports.list()
)
print(f"Found {len(list_response['data'])} imports")
print(f"Has more: {list_response['has_more']}")
for item in list_response["data"]:
    print(item)
