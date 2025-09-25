import os

import resend

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# replace with some existing audience id
audience_id: str = "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e"

create_params: resend.Broadcasts.CreateParams = {
    "audience_id": audience_id,
    "from": "onboarding@resend.dev",
    "subject": "Hello, world!",
    "html": "<p>Hello, world!</p>",
    "text": "Hello, world!",
    "reply_to": ["foo@resend.dev", "bar@resend.dev"],
    "name": "Hello, world!",
}

broadcast: resend.Broadcasts.CreateResponse = resend.Broadcasts.create(create_params)
print("Created broadcast with ID: {}".format(broadcast["id"]))
print(broadcast)

update_params: resend.Broadcasts.UpdateParams = {
    "broadcast_id": broadcast["id"],
    "html": "<p>Hello, world! Updated</p>",
    "text": "Hello, world! Updated",
    "name": "Hello, world! Updated",
}

updated_broadcast: resend.Broadcasts.UpdateResponse = resend.Broadcasts.update(
    update_params
)
print("Updated broadcast!")
print(updated_broadcast)

send_params: resend.Broadcasts.SendParams = {
    "broadcast_id": broadcast["id"],
}
sent: resend.Broadcasts.SendResponse = resend.Broadcasts.send(send_params)
print("Sent broadcast !\n")
print(sent)

retrieved: resend.Broadcast = resend.Broadcasts.get(id=broadcast["id"])
print("retrieved broadcast !\n")
print(retrieved)

if retrieved["status"] == "draft":
    removed: resend.Broadcasts.RemoveResponse = resend.Broadcasts.remove(
        id=broadcast["id"]
    )
    print("Removed broadcast !\n")
    print(removed)
    print("\n")
else:
    print("Broadcast is not in draft status, cannot remove it.\n")

list_response: resend.Broadcasts.ListResponse = resend.Broadcasts.list()
print("List of broadcasts !\n")
print(f"Found {len(list_response['data'])} broadcasts")
print(f"Has more broadcasts: {list_response['has_more']}")

print("\n--- Using pagination parameters ---")
if list_response["data"]:
    paginated_params: resend.Broadcasts.ListParams = {
        "limit": 3,
        "after": list_response["data"][0]["id"],
    }
    paginated_broadcasts: resend.Broadcasts.ListResponse = resend.Broadcasts.list(
        params=paginated_params
    )
    print(f"Retrieved {len(paginated_broadcasts['data'])} broadcasts with pagination")
    print(f"Has more broadcasts: {paginated_broadcasts['has_more']}")
else:
    print("No broadcasts available for pagination example")
