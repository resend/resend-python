import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")


# Create a new topic
create_params: resend.Topics.CreateParams = {
    "name": "Weekly Newsletter",
    "default_subscription": "opt_in",
    "description": "Subscribe to our weekly newsletter for updates",
}

topic: resend.Topics.CreateTopicResponse = resend.Topics.create(create_params)
print(f"Created topic with ID: {topic['id']}")
print(topic)

# Retrieve the topic
retrieved: resend.Topic = resend.Topics.get(topic["id"])
print("\nRetrieved topic:")
print(retrieved)

# Update the topic
update_params: resend.Topics.UpdateParams = {
    "name": "Monthly Newsletter",
    "description": "Subscribe to our monthly newsletter for updates",
}

updated: resend.Topics.UpdateTopicResponse = resend.Topics.update(
    id=topic["id"], params=update_params
)
print(f"\nUpdated topic with ID: {updated['id']}")
print(updated)

# Retrieve the updated topic to see changes
updated_topic: resend.Topic = resend.Topics.get(topic["id"])
print("\nRetrieved updated topic:")
print(updated_topic)

# List all topics
list_response: resend.Topics.ListResponse = resend.Topics.list()
print("\nList of topics:")
print(f"Found {len(list_response['data'])} topics")
print(f"Has more topics: {list_response['has_more']}")
for t in list_response["data"]:
    print(f"  - {t['name']} ({t['id']}): {t['default_subscription']}")

# List topics with pagination parameters
print("\n--- Using pagination parameters ---")
if list_response["data"]:
    paginated_params: resend.Topics.ListParams = {
        "limit": 5,
        "after": list_response["data"][0]["id"],
    }
    paginated_topics: resend.Topics.ListResponse = resend.Topics.list(
        params=paginated_params
    )
    print(f"Retrieved {len(paginated_topics['data'])} topics with pagination")
    print(f"Has more topics: {paginated_topics['has_more']}")
else:
    print("No topics available for pagination example")

# Delete the topic
removed: resend.Topics.RemoveTopicResponse = resend.Topics.remove(id=topic["id"])
print(f"\nDeleted topic with ID: {removed['id']}")
print(f"Deleted: {removed['deleted']}")
print(removed)
