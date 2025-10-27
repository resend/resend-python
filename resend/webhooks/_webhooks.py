import base64
import hmac
import time
from hashlib import sha256
from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.pagination_helper import PaginationHelper
from resend.webhooks._webhook import (VerifyWebhookOptions, Webhook,
                                      WebhookEvent, WebhookStatus)

# Default tolerance for timestamp validation (5 minutes)
DEFAULT_WEBHOOK_TOLERANCE_SECONDS = 300


class Webhooks:

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of webhooks to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more webhooks (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more webhooks (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of webhook objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[Webhook]): A list of webhook objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[Webhook]
        """
        A list of webhook objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class CreateWebhookResponse(TypedDict):
        """
        CreateWebhookResponse is the type that wraps the response of the webhook that was created

        Attributes:
            object (str): The object type, always "webhook"
            id (str): The ID of the created webhook
            signing_secret (str): The signing secret for webhook verification
        """

        object: str
        """
        The object type, always "webhook"
        """
        id: str
        """
        The ID of the created webhook
        """
        signing_secret: str
        """
        The signing secret for webhook verification
        """

    class CreateParams(TypedDict):
        endpoint: str
        """
        The URL where webhook events will be sent.
        """
        events: List[WebhookEvent]
        """
        Array of event types to subscribe to.
        See https://resend.com/docs/dashboard/webhooks/event-types for available options.
        """

    class UpdateParams(TypedDict):
        webhook_id: str
        """
        The webhook ID.
        """
        endpoint: NotRequired[str]
        """
        The URL where webhook events will be sent.
        """
        events: NotRequired[List[WebhookEvent]]
        """
        Array of event types to subscribe to.
        """
        status: NotRequired[WebhookStatus]
        """
        The webhook status. Can be either "enabled" or "disabled".
        """

    class UpdateWebhookResponse(TypedDict):
        """
        UpdateWebhookResponse is the type that wraps the response of the webhook that was updated

        Attributes:
            object (str): The object type, always "webhook"
            id (str): The ID of the updated webhook
        """

        object: str
        """
        The object type, always "webhook"
        """
        id: str
        """
        The ID of the updated webhook
        """

    class DeleteWebhookResponse(TypedDict):
        """
        DeleteWebhookResponse is the type that wraps the response of the webhook that was deleted

        Attributes:
            object (str): The object type, always "webhook"
            id (str): The ID of the deleted webhook
            deleted (bool): Whether the webhook was successfully deleted
        """

        object: str
        """
        The object type, always "webhook"
        """
        id: str
        """
        The ID of the deleted webhook
        """
        deleted: bool
        """
        Whether the webhook was successfully deleted
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateWebhookResponse:
        """
        Create a webhook to receive real-time notifications about email events.
        see more: https://resend.com/docs/api-reference/webhooks/create-webhook

        Args:
            params (CreateParams): The webhook creation parameters
                - endpoint: The URL where webhook events will be sent
                - events: Array of event types to subscribe to

        Returns:
            CreateWebhookResponse: The created webhook response with id and signing_secret
        """
        path = "/webhooks"
        resp = request.Request[Webhooks.CreateWebhookResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, webhook_id: str) -> Webhook:
        """
        Retrieve a single webhook for the authenticated user.
        see more: https://resend.com/docs/api-reference/webhooks/get-webhook

        Args:
            webhook_id (str): The webhook ID

        Returns:
            Webhook: The webhook object
        """
        path = f"/webhooks/{webhook_id}"
        resp = request.Request[Webhook](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateWebhookResponse:
        """
        Update an existing webhook configuration.
        see more: https://resend.com/docs/api-reference/webhooks/update-webhook

        Args:
            params (UpdateParams): The webhook update parameters
                - webhook_id: The webhook ID
                - endpoint: (Optional) The URL where webhook events will be sent
                - events: (Optional) Array of event types to subscribe to
                - status: (Optional) The webhook status ("enabled" or "disabled")

        Returns:
            UpdateWebhookResponse: The updated webhook response with id
        """
        webhook_id = params["webhook_id"]
        path = f"/webhooks/{webhook_id}"

        resp = request.Request[Webhooks.UpdateWebhookResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of webhooks for the authenticated user.
        see more: https://resend.com/docs/api-reference/webhooks/list-webhooks

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of webhooks to retrieve (max 100, min 1).
                  If not provided, all webhooks will be returned without pagination.
                - after: ID after which to retrieve more webhooks
                - before: ID before which to retrieve more webhooks

        Returns:
            ListResponse: A list of webhook objects
        """
        base_path = "/webhooks"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Webhooks.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, webhook_id: str) -> DeleteWebhookResponse:
        """
        Remove an existing webhook.
        see more: https://resend.com/docs/api-reference/webhooks/delete-webhook

        Args:
            webhook_id (str): The webhook ID

        Returns:
            DeleteWebhookResponse: The deleted webhook response
        """
        path = f"/webhooks/{webhook_id}"
        resp = request.Request[Webhooks.DeleteWebhookResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    def verify(cls, options: VerifyWebhookOptions) -> None:
        """
        Verify validates a webhook payload using HMAC-SHA256 signature verification.
        This implements manual verification without external dependencies.
        see more: https://docs.svix.com/receiving/verifying-payloads/how-manual

        Args:
            options (VerifyWebhookOptions): The webhook verification parameters
                - payload: The raw request body as a string
                - headers: The Svix headers (svix-id, svix-timestamp, svix-signature)
                - webhook_secret: The webhook signing secret (starts with whsec_)

        Raises:
            ValueError: If verification fails or required parameters are missing

        Returns:
            None: Returns None on successful verification, raises ValueError otherwise
        """
        # Validate required parameters
        if not options:
            raise ValueError("options cannot be None")

        if not options.get("payload"):
            raise ValueError("payload cannot be empty")

        if not options.get("webhook_secret"):
            raise ValueError("webhook_secret cannot be empty")

        headers = options.get("headers")
        if not headers:
            raise ValueError("headers are required")

        if not headers.get("id"):
            raise ValueError("svix-id header is required")

        if not headers.get("timestamp"):
            raise ValueError("svix-timestamp header is required")

        if not headers.get("signature"):
            raise ValueError("svix-signature header is required")

        # Step 1: Validate timestamp to prevent replay attacks
        try:
            timestamp = int(headers["timestamp"])
        except (ValueError, TypeError) as e:
            raise ValueError(f"invalid timestamp format: {e}")

        now = int(time.time())
        diff = now - timestamp
        if (
            diff > DEFAULT_WEBHOOK_TOLERANCE_SECONDS
            or diff < -DEFAULT_WEBHOOK_TOLERANCE_SECONDS
        ):
            raise ValueError(
                f"timestamp outside tolerance window: difference of {diff} seconds"
            )

        # Step 2: Construct signed content: {id}.{timestamp}.{payload}
        signed_content = f"{headers['id']}.{headers['timestamp']}.{options['payload']}"

        # Step 3: Decode the signing secret (strip whsec_ prefix and base64 decode)
        secret = options["webhook_secret"]
        if secret.startswith("whsec_"):
            secret = secret[6:]  # Remove "whsec_" prefix

        try:
            decoded_secret = base64.b64decode(secret)
        except Exception as e:
            raise ValueError(f"failed to decode webhook secret: {e}")

        # Step 4: Calculate expected signature using HMAC-SHA256
        expected_signature = cls._generate_signature(
            decoded_secret, signed_content.encode("utf-8")
        )

        # Step 5: Compare signatures using constant-time comparison
        # The signature header contains space-separated signatures with version prefixes
        # (e.g., "v1,sig1 v1,sig2")
        signatures = headers["signature"].split(" ")
        for sig in signatures:
            # Strip version prefix (e.g., "v1,")
            parts = sig.split(",", 1)
            if len(parts) != 2:
                continue

            received_signature = parts[1]
            if hmac.compare_digest(expected_signature, received_signature):
                return  # Signature matches

        raise ValueError("no matching signature found")

    @staticmethod
    def _generate_signature(secret: bytes, content: bytes) -> str:
        """
        Generate an HMAC-SHA256 signature and return it as base64.

        Args:
            secret (bytes): The decoded webhook secret
            content (bytes): The content to sign

        Returns:
            str: The base64-encoded signature
        """
        h = hmac.new(secret, content, sha256)
        signature = h.digest()
        return base64.b64encode(signature).decode("utf-8")
