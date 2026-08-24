from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import Literal, NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.emails._attachment import Attachment, RemoteAttachment
from resend.emails._attachments import Attachments
from resend.emails._email import Email
from resend.emails._receiving import Receiving
from resend.emails._tag import Tag
from resend.pagination_helper import PaginationHelper

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass

MetricsGranularity = Literal["hourly", "daily", "weekly", "monthly"]

MetricsMetric = Literal[
    "received",
    "delivered",
    "complained",
    "suppressed",
    "bounced",
    "bounced_transient",
    "bounced_permanent",
    "bounced_undetermined",
    "opened",
    "clicked",
    "unsubscribed",
    "delivery_delayed",
    "failed",
    "sent",
    "unique_opened",
    "unique_clicked",
    "delivery_rate",
    "open_rate",
    "click_rate",
    "bounce_rate",
    "complaint_rate",
    "unsubscribe_rate",
]

MetricsDimension = Literal["period", "domain", "email", "broadcast"]


class EmailTemplate(TypedDict):
    """
    EmailTemplate is the class that wraps template configuration for email sending.

    Attributes:
        id (str): The template ID.
        variables (NotRequired[Dict[str, Union[str, int]]]): Optional variables to be used in the template.
    """

    id: str
    """
    The template ID.
    """
    variables: NotRequired[Dict[str, Union[str, int]]]
    """
    Optional variables to be used in the template.
    """


class _UpdateParams(TypedDict):
    id: str
    """
    The ID of the email to update.
    """
    scheduled_at: NotRequired[str]
    """
    Schedule email to be sent later.
    The date should be in ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
    """


class _UpdateEmailResponse(BaseResponse):
    object: str
    """
    The object type: email
    """
    id: str
    """
    The ID of the scheduled email that was canceled.
    """


class _CancelScheduledEmailResponse(BaseResponse):
    object: str
    """
    The object type: email
    """
    id: str
    """
    The ID of the scheduled email that was canceled.
    """


class _ShareParams(TypedDict):
    expires_in: NotRequired[str]
    """
    A human-readable duration for how long the share link stays valid
    (e.g. "10m", "2 hours", "1 day", "1h 30m"). Defaults to "48h".
    Capped at 48 hours.
    """


class _ShareEmailResponse(BaseResponse):
    object: str
    """
    The object type: email
    """
    id: str
    """
    The ID of the email that was shared.
    """
    url: str
    """
    The shareable link URL.
    """


class _MetricsParams(TypedDict):
    start_date: NotRequired[str]
    """
    Start of the date range, as an ISO 8601 date or datetime.
    Defaults to 6 days before end_date.
    """
    end_date: NotRequired[str]
    """
    End of the date range, as an ISO 8601 date or datetime.
    Defaults to now.
    """
    timezone: NotRequired[str]
    """
    IANA timezone (e.g. "America/New_York") used to bucket results.
    Defaults to "UTC".
    """
    granularity: NotRequired[MetricsGranularity]
    """
    The bucket size used for the "period" dimension. Defaults to "daily".
    """
    metrics: NotRequired[List[MetricsMetric]]
    """
    The metrics to compute. Defaults to all available metrics.
    """
    dimensions: NotRequired[List[MetricsDimension]]
    """
    The dimensions to break results down by. Defaults to no dimensions, in
    which case only `totals` is returned and `data` is omitted.
    Note: the "email" and "broadcast" dimensions cannot be combined
    (raises ValueError before the request is sent).
    """
    domain_id: NotRequired[List[str]]
    """
    Restrict results to these sending domain IDs. Maximum 100.
    """
    email_id: NotRequired[List[str]]
    """
    Restrict results to these email IDs. Maximum 100.
    Cannot be combined with the "broadcast" dimension or broadcast_id filter
    (raises ValueError before the request is sent).
    """
    broadcast_id: NotRequired[List[str]]
    """
    Restrict results to these broadcast IDs. Maximum 100.
    Cannot be combined with the "email" dimension or email_id filter
    (raises ValueError before the request is sent).
    """


class _MetricsResponse(BaseResponse):
    object: str
    """
    The object type: "metrics"
    """
    start_date: str
    """
    Start of the date range that was queried.
    """
    end_date: str
    """
    End of the date range that was queried.
    """
    metrics: List[str]
    """
    The metrics that were computed.
    """
    dimensions: List[str]
    """
    The dimensions results are broken down by.
    """
    granularity: str
    """
    The bucket size used for the "period" dimension.
    """
    totals: Dict[str, Any]
    """
    The requested metrics, totaled across the whole date range.
    """
    data: NotRequired[List[Dict[str, Any]]]
    """
    One row per combination of requested dimensions, each containing the
    dimension key fields (e.g. `period`, `domain_id`/`domain_name`,
    `email_id`, `broadcast_id`/`broadcast_name`) plus the requested metrics.
    Omitted when `dimensions` is empty.
    """


# SendParamsFrom is declared with functional TypedDict syntax here because
# "from" is a reserved keyword in Python, and this is the best way to
# support type-checking for it.
_SendParamsFrom = TypedDict(
    "_SendParamsFrom",
    {
        "from": NotRequired[str],
    },
)


class _SendParamsDefault(_SendParamsFrom):
    to: Union[str, List[str]]
    """
    List of email addresses to send the email to.
    """
    subject: NotRequired[str]
    """
    The subject of the email.
    """
    bcc: NotRequired[Union[List[str], str]]
    """
    Bcc
    """
    cc: NotRequired[Union[List[str], str]]
    """
    Cc
    """
    reply_to: NotRequired[Union[List[str], str]]
    """
    Reply to
    """
    html: NotRequired[str]
    """
    The HTML content of the email.
    """
    text: NotRequired[str]
    """
    The text content of the email.
    """
    headers: NotRequired[Dict[str, str]]
    """
    Custom headers to be added to the email.
    """
    attachments: NotRequired[List[Union[Attachment, RemoteAttachment]]]
    """
    List of attachments to be added to the email.
    """
    tags: NotRequired[List[Tag]]
    """
    List of tags to be added to the email.
    """
    scheduled_at: NotRequired[str]
    """
    Schedule email to be sent later.
    The date should be in ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
    """
    template: NotRequired[EmailTemplate]
    """
    Template configuration for sending emails using predefined templates.
    """


def _validate_metrics_params(params: Optional["Emails.MetricsParams"]) -> None:
    if not params:
        return
    dimensions = params.get("dimensions") or []
    has_broadcast = "broadcast" in dimensions or bool(params.get("broadcast_id"))
    has_email = "email" in dimensions or bool(params.get("email_id"))
    if has_broadcast and has_email:
        raise ValueError(
            "the broadcast dimension/broadcast_id filter cannot be combined "
            "with the email dimension/email_id filter"
        )


def _build_metrics_query_params(
    params: Optional["Emails.MetricsParams"],
) -> Optional[Dict[str, Any]]:
    """
    Comma-join list-valued params (metrics, dimensions, domain_id, email_id,
    broadcast_id) the way the metrics endpoint expects them in the query
    string; PaginationHelper.build_paginated_path does not join lists itself.
    """
    if not params:
        return None
    return {
        key: ",".join(value) if isinstance(value, list) else value
        for key, value in params.items()
        if not (isinstance(value, list) and not value)
    }


class Emails:
    Attachments = Attachments
    Receiving = Receiving

    class CancelScheduledEmailResponse(_CancelScheduledEmailResponse):
        """
        CancelScheduledEmailResponse is the type that wraps the response of the email that was canceled

        Attributes:
            object (str): The object type
            id (str): The ID of the scheduled email that was canceled
        """

    class UpdateEmailResponse(_UpdateEmailResponse):
        """
        UpdateEmailResponse is the type for the updated email response.

        Attributes:
            object (str): The object type
            id (str): The ID of the updated email.
        """

    class ShareParams(_ShareParams):
        """
        ShareParams is the class that wraps the parameters for the share method.

        Attributes:
            expires_in (NotRequired[str]): A human-readable duration for how long \
            the share link stays valid (e.g. "10m", "2 hours", "1 day", "1h 30m"). \
            Defaults to "48h". Capped at 48 hours.
        """

    class ShareEmailResponse(_ShareEmailResponse):
        """
        ShareEmailResponse is the type that wraps the response of a shared email link.

        Attributes:
            object (str): The object type
            id (str): The ID of the email that was shared.
            url (str): The shareable link URL.
        """

    class MetricsParams(_MetricsParams):
        """
        MetricsParams is the class that wraps the parameters for the metrics method.

        Attributes:
            start_date (NotRequired[str]): Start of the date range (ISO 8601). \
            Defaults to 6 days before end_date.
            end_date (NotRequired[str]): End of the date range (ISO 8601). Defaults to now.
            timezone (NotRequired[str]): IANA timezone, e.g. "America/New_York". Defaults to "UTC".
            granularity (NotRequired[MetricsGranularity]): Bucket size for the "period" \
            dimension. Defaults to "daily".
            metrics (NotRequired[List[MetricsMetric]]): The metrics to compute. \
            Defaults to all available metrics.
            dimensions (NotRequired[List[MetricsDimension]]): The dimensions to break \
            results down by. Defaults to none, in which case only `totals` is returned.
            domain_id (NotRequired[List[str]]): Restrict results to these sending domain IDs.
            email_id (NotRequired[List[str]]): Restrict results to these email IDs.
            broadcast_id (NotRequired[List[str]]): Restrict results to these broadcast IDs.
        """

    class MetricsResponse(_MetricsResponse):
        """
        MetricsResponse is the type that wraps the response of the metrics method.

        Attributes:
            object (str): The object type: "metrics"
            start_date (str): Start of the date range that was queried.
            end_date (str): End of the date range that was queried.
            metrics (List[str]): The metrics that were computed.
            dimensions (List[str]): The dimensions results are broken down by.
            granularity (str): The bucket size used for the "period" dimension.
            totals (Dict[str, Any]): The requested metrics, totaled across the whole date range.
            data (NotRequired[List[Dict[str, Any]]]): One row per combination of requested \
            dimensions. Omitted when `dimensions` is empty.
        """

    class UpdateParams(_UpdateParams):
        """
        UpdateParams is the class that wraps the parameters for the update method.

        Attributes:
            id (str): The ID of the email to update.
            scheduled_at (NotRequired[str]): Schedule email to be sent later. \
            The date should be in ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
        """

    class SendParams(_SendParamsDefault):
        """SendParams is the class that wraps the parameters for the send method.

        Attributes:
            from (NotRequired[str]): The email address to send the email from.
            to (Union[str, List[str]]): List of email addresses to send the email to.
            subject (NotRequired[str]): The subject of the email.
            bcc (NotRequired[Union[List[str], str]]): Bcc
            cc (NotRequired[Union[List[str], str]]): Cc
            reply_to (NotRequired[Union[List[str], str]]): Reply to
            html (NotRequired[str]): The HTML content of the email.
            text (NotRequired[str]): The text content of the email.
            headers (NotRequired[Dict[str, str]]): Custom headers to be added to the email.
            attachments (NotRequired[List[Union[Attachment, RemoteAttachment]]]): List of attachments to be added to the email.
            tags (NotRequired[List[Tag]]): List of tags to be added to the email.
            template (NotRequired[EmailTemplate]): Template configuration for sending emails using predefined templates.
        """

    class SendOptions(TypedDict):
        """
        SendOptions is the class that wraps the options for the send method.

        Attributes:
            idempotency_key (NotRequired[str]): Unique key that ensures the same operation is not processed multiple times.
            Allows for safe retries without duplicating operations.
            If provided, will be sent as the `Idempotency-Key` header.
        """

        idempotency_key: NotRequired[str]
        """
        Unique key that ensures the same operation is not processed multiple times.
        Allows for safe retries without duplicating operations.
        If provided, will be sent as the `Idempotency-Key` header.
        """

    class SendResponse(BaseResponse):
        """
        SendResponse is the type that wraps the response of the email that was sent.

        Attributes:
            id (str): The ID of the sent email
            http_headers (NotRequired[Dict[str, str]]): HTTP response headers (inherited from BaseResponse)
        """

        id: str
        """
        The sent Email ID.
        """

    class ListParams(TypedDict):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            limit (NotRequired[int]): The maximum number of emails to return. Defaults to 10, maximum 100.
            after (NotRequired[str]): Return emails after this cursor for pagination.
            before (NotRequired[str]): Return emails before this cursor for pagination.
        """

        limit: NotRequired[int]
        """
        The maximum number of emails to return. Defaults to 10, maximum 100.
        """
        after: NotRequired[str]
        """
        Return emails after this cursor for pagination.
        """
        before: NotRequired[str]
        """
        Return emails before this cursor for pagination.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is the type that wraps the response for listing emails.

        Attributes:
            object (str): The object type: "list"
            data (List[Email]): The list of email objects.
            has_more (bool): Whether there are more emails available for pagination.
            http_headers (NotRequired[Dict[str, str]]): HTTP response headers (inherited from BaseResponse)
        """

        object: str
        """
        The object type: "list"
        """
        data: List[Email]
        """
        The list of email objects.
        """
        has_more: bool
        """
        Whether there are more emails available for pagination.
        """

    @classmethod
    def send(
        cls, params: SendParams, options: Optional[SendOptions] = None
    ) -> SendResponse:
        """
        Send an email through the Resend Email API.
        see more: https://resend.com/docs/api-reference/emails/send-email

        Args:
            params (SendParams): The email parameters
            options (SendOptions): The email options

        Returns:
            id: The ID of the sent email
        """
        path = "/emails"
        resp = request.Request[Emails.SendResponse](
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, email_id: str) -> Email:
        """
        Retrieve a single email.
        see more: https://resend.com/docs/api-reference/emails/retrieve-email

        Args:
            email_id (str): The ID of the email to retrieve

        Returns:
            Email: The email object that was retrieved
        """
        path = f"/emails/{email_id}"
        resp = request.Request[Email](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    def cancel(cls, email_id: str) -> CancelScheduledEmailResponse:
        """
        Cancel a scheduled email.
        see more: https://resend.com/docs/api-reference/emails/cancel-email

        Args:
            email_id (str): The ID of the scheduled email to cancel

        Returns:
            CancelScheduledEmailResponse: The response object that contains the ID of the scheduled email that was canceled
        """
        path = f"/emails/{email_id}/cancel"
        resp = request.Request[_CancelScheduledEmailResponse](
            path=path,
            params={},
            verb="post",
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateEmailResponse:
        """
        Update an email.
        see more: https://resend.com/docs/api-reference/emails/update-email

        Args:
            params (UpdateParams): The email parameters to update

        Returns:
            Email: The email object that was updated
        """
        path = f"/emails/{params['id']}"
        resp = request.Request[_UpdateEmailResponse](
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="patch",
        ).perform_with_content()
        return resp

    @classmethod
    def share(
        cls, email_id: str, params: Optional[ShareParams] = None
    ) -> ShareEmailResponse:
        """
        Create a shareable link for an email.
        see more: https://resend.com/docs/api-reference/emails/share-email

        Args:
            email_id (str): The ID of the email (sent or received) to share
            params (Optional[ShareParams]): The share parameters

        Returns:
            ShareEmailResponse: The response object that contains the shareable link URL
        """
        path = f"/emails/{email_id}/share"
        resp = request.Request[_ShareEmailResponse](
            path=path,
            params=cast(Dict[Any, Any], params) if params else {},
            verb="post",
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of emails.
        see more: https://resend.com/docs/api-reference/emails/list-emails

        Args:
            params (Optional[ListParams]): The list parameters for pagination

        Returns:
            ListResponse: A paginated list of email objects
        """
        base_path = "/emails"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Emails.ListResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    def metrics(cls, params: Optional[MetricsParams] = None) -> MetricsResponse:
        """
        Retrieve email metrics.
        see more: https://resend.com/docs/api-reference/emails/get-metrics

        Args:
            params (Optional[MetricsParams]): The metrics query parameters

        Returns:
            MetricsResponse: The requested metrics, totaled and (optionally) broken down by dimension
        """
        _validate_metrics_params(params)
        base_path = "/emails/metrics"
        query_params = _build_metrics_query_params(params)
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Emails.MetricsResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    async def send_async(
        cls, params: SendParams, options: Optional[SendOptions] = None
    ) -> SendResponse:
        """
        Send an email through the Resend Email API (async version).
        see more: https://resend.com/docs/api-reference/emails/send-email

        Args:
            params (SendParams): The email parameters
            options (SendOptions): The email options

        Returns:
            SendResponse: The send response with the email ID
        """
        path = "/emails"
        resp = await AsyncRequest[Emails.SendResponse](
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, email_id: str) -> Email:
        """
        Retrieve a single email (async version).
        see more: https://resend.com/docs/api-reference/emails/retrieve-email

        Args:
            email_id (str): The ID of the email to retrieve

        Returns:
            Email: The email object that was retrieved
        """
        path = f"/emails/{email_id}"
        resp = await AsyncRequest[Email](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of emails (async version).
        see more: https://resend.com/docs/api-reference/emails/list-emails

        Args:
            params (Optional[ListParams]): The list parameters for pagination

        Returns:
            ListResponse: A paginated list of email objects
        """
        base_path = "/emails"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = await AsyncRequest[Emails.ListResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    async def metrics_async(
        cls, params: Optional[MetricsParams] = None
    ) -> MetricsResponse:
        """
        Retrieve email metrics (async version).
        see more: https://resend.com/docs/api-reference/emails/get-metrics

        Args:
            params (Optional[MetricsParams]): The metrics query parameters

        Returns:
            MetricsResponse: The requested metrics, totaled and (optionally) broken down by dimension
        """
        _validate_metrics_params(params)
        base_path = "/emails/metrics"
        query_params = _build_metrics_query_params(params)
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = await AsyncRequest[Emails.MetricsResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    async def cancel_async(cls, email_id: str) -> CancelScheduledEmailResponse:
        """
        Cancel a scheduled email (async version).
        see more: https://resend.com/docs/api-reference/emails/cancel-email

        Args:
            email_id (str): The ID of the scheduled email to cancel

        Returns:
            CancelScheduledEmailResponse: The response object that contains the ID of the scheduled email that was canceled
        """
        path = f"/emails/{email_id}/cancel"
        resp = await AsyncRequest[_CancelScheduledEmailResponse](
            path=path,
            params={},
            verb="post",
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> UpdateEmailResponse:
        """
        Update an email (async version).
        see more: https://resend.com/docs/api-reference/emails/update-email

        Args:
            params (UpdateParams): The email parameters to update

        Returns:
            Email: The email object that was updated
        """
        path = f"/emails/{params['id']}"
        resp = await AsyncRequest[_UpdateEmailResponse](
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="patch",
        ).perform_with_content()
        return resp

    @classmethod
    async def share_async(
        cls, email_id: str, params: Optional[ShareParams] = None
    ) -> ShareEmailResponse:
        """
        Create a shareable link for an email (async version).
        see more: https://resend.com/docs/api-reference/emails/share-email

        Args:
            email_id (str): The ID of the email (sent or received) to share
            params (Optional[ShareParams]): The share parameters

        Returns:
            ShareEmailResponse: The response object that contains the shareable link URL
        """
        path = f"/emails/{email_id}/share"
        resp = await AsyncRequest[_ShareEmailResponse](
            path=path,
            params=cast(Dict[Any, Any], params) if params else {},
            verb="post",
        ).perform_with_content()
        return resp
