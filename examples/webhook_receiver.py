"""
Webhook Receiver Example

Demonstrates how to receive and verify webhooks from Resend.
This example creates an HTTP server that listens for webhook POST requests
and verifies them using HMAC-SHA256 signature validation.

Requirements:
    pip install flask

Usage:
    1. Set your webhook secret (get it when creating a webhook)
    2. Run: python examples/webhook_receiver.py
    3. Send a POST request with Resend webhook headers to test verification

Note:
    For local testing, you can use tools like ngrok to expose your local server:
    ngrok http 5000
    Then use the ngrok URL when creating your webhook in Resend.
"""

# mypy: ignore-errors

import json
import os
from typing import Dict, Tuple, Union

from flask import Flask, request

import resend

app = Flask(__name__)

# Get webhook secret from environment or use a placeholder
WEBHOOK_SECRET = os.getenv(
    "RESEND_WEBHOOK_SECRET", "whsec_zC+p1uXQxsAgZfH0SxB3lrl1DcSb4iPX"
)


@app.route("/webhook", methods=["POST"])
def webhook_handler() -> Tuple[Dict[str, Union[str, bool]], int]:
    """
    Handle incoming webhook requests from Resend.
    Verifies the webhook signature and processes the event.
    """
    # Read the raw body (must be raw for signature verification)
    body = request.get_data(as_text=True)

    # Extract Svix headers
    headers: resend.WebhookHeaders = {
        "id": request.headers.get("svix-id", ""),
        "timestamp": request.headers.get("svix-timestamp", ""),
        "signature": request.headers.get("svix-signature", ""),
    }

    # Verify the webhook
    try:
        resend.Webhooks.verify(
            {
                "payload": body,
                "headers": headers,
                "webhook_secret": WEBHOOK_SECRET,
            }
        )
    except ValueError as e:
        print(f"Webhook verification failed: {e}")
        return {"error": "Webhook verification failed"}, 400

    # Parse the verified payload
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"error": "Invalid JSON payload"}, 400

    # Process the webhook event
    event_type = payload.get("type")
    print("✓ Webhook verified successfully!")
    print(f"Event Type: {event_type}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    print(f"Event: {payload.get('data', {}).get('email_id')}")

    return {"success": True}, 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Webhook receiver listening on http://localhost:{port}/webhook")
    print("Send a POST request with Resend webhook headers to test verification")
    print(f"Using webhook secret: {WEBHOOK_SECRET[:15]}...")
    app.run(host="0.0.0.0", port=port, debug=True)
