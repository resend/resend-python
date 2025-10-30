import os
from typing import List

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# replace with some audience id
audience_id: str = "ca4e37c5-a82a-4199-a3b8-bf912a6472aa"

create_params: resend.Contacts.CreateParams = {
    "audience_id": audience_id,
    "email": "sw@exmple.com",
    "first_name": "Steve",
    "last_name": "Wozniak",
    "unsubscribed": False,
}

contact: resend.Contacts.CreateContactResponse = resend.Contacts.create(create_params)
print("Created contact with ID: {}".format(contact["id"]))
print(contact)

update_params: resend.Contacts.UpdateParams = {
    "audience_id": audience_id,
    "id": contact["id"],
    "unsubscribed": False,
    "first_name": "Steve",
}

updated: resend.Contacts.UpdateContactResponse = resend.Contacts.update(update_params)
print("updated contact with ID: {}".format(updated["id"]))
print(updated)

cont_by_id: resend.Contact = resend.Contacts.get(
    id=contact["id"], audience_id=audience_id
)
print("Retrieved contact by ID")
print(cont_by_id)

cont_by_email: resend.Contact = resend.Contacts.get(
    email="sw@exmple.com", audience_id=audience_id
)
print("Retrieved contact by Email")
print(cont_by_email)

contacts: resend.Contacts.ListResponse = resend.Contacts.list(audience_id=audience_id)
print("List of contacts")
print(f"Found {len(contacts['data'])} contacts")
print(f"Has more contacts: {contacts['has_more']}")
for c in contacts["data"]:
    print(c)

print("\n--- Using pagination parameters ---")
if contacts["data"]:
    paginated_params: resend.Contacts.ListParams = {
        "limit": 2,
        "after": contacts["data"][0]["id"],
    }
    paginated_contacts: resend.Contacts.ListResponse = resend.Contacts.list(
        audience_id=audience_id, params=paginated_params
    )
    print(f"Retrieved {len(paginated_contacts['data'])} contacts with pagination")
    print(f"Has more contacts: {paginated_contacts['has_more']}")
else:
    print("No contacts available for pagination example")

print("\n--- Contact Topics Examples ---")

print("\nCreating a topic...")
topic_create_params: resend.Topics.CreateParams = {
    "name": "Product Updates",
    "default_subscription": "opt_in",
    "description": "Latest product updates and features",
}
created_topic: resend.Topics.CreateTopicResponse = resend.Topics.create(
    topic_create_params
)
print(f"Created topic with ID: {created_topic['id']}")

topic_create_params_2: resend.Topics.CreateParams = {
    "name": "Newsletter",
    "default_subscription": "opt_out",
    "description": "Weekly newsletter",
}
created_topic_2: resend.Topics.CreateTopicResponse = resend.Topics.create(
    topic_create_params_2
)
print(f"Created topic with ID: {created_topic_2['id']}")

print("\nListing topics for contact by ID...")
topics_response: resend.ContactsTopics.ListResponse = resend.Contacts.Topics.list(
    contact_id=contact["id"]
)
print(f"Found {len(topics_response['data'])} topics for contact")
for topic in topics_response["data"]:
    print(f"  - {topic['name']}: {topic['subscription']}")

print("\nListing topics for contact by email...")
topics_by_email: resend.ContactsTopics.ListResponse = resend.Contacts.Topics.list(
    email="sw@exmple.com"
)
print(f"Found {len(topics_by_email['data'])} topics for contact")

# Update topic subscriptions for a contact by ID
print("\nUpdating topic subscriptions by contact ID...")
update_topics_params: resend.ContactsTopics.UpdateParams = {
    "id": contact["id"],
    "topics": [
        {"id": created_topic["id"], "subscription": "opt_in"},
        {"id": created_topic_2["id"], "subscription": "opt_out"},
    ],
}
update_topics_response: resend.ContactsTopics.UpdateResponse = (
    resend.Contacts.Topics.update(update_topics_params)
)
print(f"Updated topics for contact: {update_topics_response['id']}")

# Update topic subscriptions for a contact by email
print("\nUpdating topic subscriptions by contact email...")
update_topics_by_email: resend.ContactsTopics.UpdateParams = {
    "email": "sw@exmple.com",
    "topics": [
        {"id": created_topic["id"], "subscription": "opt_in"},
        {"id": created_topic_2["id"], "subscription": "opt_in"},
    ],
}
update_by_email_response: resend.ContactsTopics.UpdateResponse = (
    resend.Contacts.Topics.update(update_topics_by_email)
)
print(f"Updated topics for contact by email: {update_by_email_response['id']}")

# List topics again to see the updates
print("\nListing topics after updates...")
updated_topics: resend.ContactsTopics.ListResponse = resend.Contacts.Topics.list(
    contact_id=contact["id"]
)
for topic in updated_topics["data"]:
    print(f"  - {topic['name']}: {topic['subscription']}")

# Clean up: remove the topics we created
print("\nCleaning up topics...")
resend.Topics.remove(created_topic["id"])
resend.Topics.remove(created_topic_2["id"])
print("Topics removed")

# remove by email
rmed: resend.Contacts.RemoveContactResponse = resend.Contacts.remove(
    audience_id=audience_id, email=cont_by_email["email"]
)

# remove by id
# rmed: resend.Contacts.RemoveContactResponse = resend.Contacts.remove(audience_id=audience_id, id=cont["id"])

print(f"Removed contact with ID: {rmed['contact']}")
print(rmed)
