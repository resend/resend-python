"""Example usage of the Templates API."""

import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Define template variables with explicit typing
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

# Create a new template with variables
create_params: resend.Templates.CreateParams = {
    "name": "welcome-email",
    "html": "<strong>Hey, {{{NAME}}}, you are {{{AGE}}} years old.</strong>",
    "variables": variables,
}

template: resend.Templates.CreateResponse = resend.Templates.create(create_params)
print(f"Created template: {template['id']}")

# Publish the template to make it available for use
published: resend.Templates.PublishResponse = resend.Templates.publish(template["id"])
print(f"Published template: {published['id']}")

# Duplicate a template
duplicated: resend.Templates.DuplicateResponse = resend.Templates.duplicate(
    template["id"]
)
print(f"Duplicated template: {duplicated['id']}")

# Get a template by ID
retrieved_template: resend.Template = resend.Templates.get(template["id"])
print(f"Retrieved template: {retrieved_template['name']}")

# Update a template (update just the name, keep HTML/variables the same)
update_params: resend.Templates.UpdateParams = {
    "id": template["id"],
    "name": "updated-welcome-email",
}
updated: resend.Templates.UpdateResponse = resend.Templates.update(update_params)
print(f"Updated template: {updated['id']}")

# List all templates with pagination
list_params: resend.Templates.ListParams = {
    "limit": 10,
}
templates: resend.Templates.ListResponse = resend.Templates.list(list_params)
print(f"Total templates: {len(templates['data'])}")
for t in templates["data"]:
    print(f"  - {t['name']} ({t['id']})")

# Delete templates (cleanup)
removed: resend.Templates.RemoveResponse = resend.Templates.remove(template["id"])
print(f"Deleted template: {removed['id']}, deleted={removed['deleted']}")

removed_dup: resend.Templates.RemoveResponse = resend.Templates.remove(duplicated["id"])
print(
    f"Deleted duplicated template: {removed_dup['id']}, deleted={removed_dup['deleted']}"
)
