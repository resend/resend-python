import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

create_response = resend.ContactProperties.create(
    {
        "key": "age",
        "type": "number",
        "fallback_value": 0,
    }
)
print(f"Created contact property: {create_response}")

list_response = resend.ContactProperties.list()
print(f"Contact properties: {list_response}")

paginated_response = resend.ContactProperties.list({"limit": 10})
print(f"Limited contact properties: {paginated_response}")
print(f"Has more: {paginated_response.get('has_more', False)}")

property_id = create_response["id"]
property_details = resend.ContactProperties.get(property_id)
print(f"Contact property details: {property_details}")

update_response = resend.ContactProperties.update(
    {"id": property_id, "fallback_value": 18}
)
print(f"Updated contact property: {update_response}")

remove_response = resend.ContactProperties.remove(property_id)
print(f"Removed contact property: {remove_response}")
