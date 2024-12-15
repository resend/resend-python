import os
from typing import List

import resend
import resend.broadcasts

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

# replace with some existing audience id
audience_id: str = "78b8d3bc-a55a-45a3-aee6-6ec0a5e13d7e"

create_params: resend.Broadcasts.CreateParams = {
    "audience_id": audience_id,
    "from": "hi@presenteia.se",
    "subject": "Hello, world!",
    "html": "<p>Hello, world!</p>",
    "text": "Hello, world!",
    "reply_to": ["lel@lel.com", "lil@lil.com"],
    "name": "Hello, world!",
}

broadcast: resend.CreateBroadcastResponse = resend.Broadcasts.create(create_params)
print("Created broadcast !")
print(broadcast)

retrieved: resend.Broadcast = resend.Broadcasts.get(id=broadcast["id"])
print("retrieved broadcast !")
print(retrieved)

send_params: resend.Broadcasts.SendParams = {
    "broadcast_id": broadcast["id"],
}
sent: resend.SendBroadcastResponse = resend.Broadcasts.send(send_params)
print("Sent broadcast !")
print(sent)
