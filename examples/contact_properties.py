import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# Create a contact property
create_params: resend.ContactProperties.CreateParams = {
    "key": "age",
    "type": "number",
    "fallback_value": 0,
}
create_response: resend.ContactProperties.CreateResponse = (
    resend.ContactProperties.create(create_params)
)
print(f"Created contact property: {create_response}")

# List all contact properties
list_response: resend.ContactProperties.ListResponse = resend.ContactProperties.list()
print(f"Contact properties: {list_response}")

# List with pagination
list_params: resend.ContactProperties.ListParams = {"limit": 10}
paginated_response: resend.ContactProperties.ListResponse = (
    resend.ContactProperties.list(list_params)
)
print(f"Limited contact properties: {paginated_response}")
print(f"Has more: {paginated_response.get('has_more', False)}")

# Get a specific contact property
property_id: str = create_response["id"]
property_details: resend.ContactProperty = resend.ContactProperties.get(property_id)
print(f"Contact property details: {property_details}")

# Update a contact property
update_params: resend.ContactProperties.UpdateParams = {
    "id": property_id,
    "fallback_value": 18,
}
update_response: resend.ContactProperties.UpdateResponse = (
    resend.ContactProperties.update(update_params)
)
print(f"Updated contact property: {update_response}")

# Remove a contact property
remove_response: resend.ContactProperties.RemoveResponse = (
    resend.ContactProperties.remove(property_id)
)
print(f"Removed contact property: {remove_response}")
