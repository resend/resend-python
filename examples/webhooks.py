import os
from typing import List

import resend
from resend.webhooks import WebhookEvent

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing")

events: List[WebhookEvent] = ["email.sent", "email.delivered", "email.bounced"]

create_params: resend.Webhooks.CreateParams = {
    "endpoint": "https://webhook.example.com/handler",
    "events": events,
}
webhook: resend.Webhooks.CreateWebhookResponse = resend.Webhooks.create(
    params=create_params
)
print(f"Created webhook: {webhook['id']}")
print(f"Signing secret: {webhook['signing_secret']}")
print(webhook)

retrieved: resend.Webhook = resend.Webhooks.get(webhook_id=webhook["id"])
print(f"Retrieved webhook: {retrieved['id']}")
print(f"Endpoint: {retrieved['endpoint']}")
print(f"Events: {retrieved['events']}")
print(f"Status: {retrieved['status']}")

update_params: resend.Webhooks.UpdateParams = {
    "webhook_id": webhook["id"],
    "endpoint": "https://new-webhook.example.com/handler",
    "events": ["email.sent", "email.delivered"],
    "status": "enabled",
}

updated_webhook: resend.Webhooks.UpdateWebhookResponse = resend.Webhooks.update(
    update_params
)
print(f"Updated webhook: {updated_webhook['id']}")

webhooks: resend.Webhooks.ListResponse = resend.Webhooks.list()
print(f"Found {len(webhooks['data'])} webhooks")
print(f"Has more webhooks: {webhooks['has_more']}")
if not webhooks["data"]:
    print("No webhooks found")
for hook in webhooks["data"]:
    print(hook)

print("\n--- Using pagination parameters ---")
if webhooks["data"]:
    paginated_params: resend.Webhooks.ListParams = {
        "limit": 5,
        "after": webhooks["data"][0]["id"],
    }
    paginated_webhooks: resend.Webhooks.ListResponse = resend.Webhooks.list(
        params=paginated_params
    )
    print(f"Retrieved {len(paginated_webhooks['data'])} webhooks with pagination")
    print(f"Has more webhooks: {paginated_webhooks['has_more']}")
else:
    print("No webhooks available for pagination example")

rm_webhook: resend.Webhooks.DeleteWebhookResponse = resend.Webhooks.remove(
    webhook_id=webhook["id"]
)
print(f"Deleted webhook: {rm_webhook['id']}")
print(f"Deleted: {rm_webhook['deleted']}")
print(rm_webhook)
