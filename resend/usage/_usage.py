from typing import Union

from typing_extensions import TypedDict

from resend import request
from resend._base_response import BaseResponse

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class EmailsDailyUsage(TypedDict):
    """
    EmailsDailyUsage is the type that wraps the caller's daily email usage.

    Attributes:
        used (int): The number of emails counted against the daily quota
        limit (Union[int, None]): The daily email quota, or None if unlimited
        sent (int): The number of emails sent today
        received (int): The number of emails received today
        resets_at (str): When the daily quota resets, as an ISO 8601 datetime
    """

    used: int
    """
    The number of emails counted against the daily quota.
    """
    limit: Union[int, None]
    """
    The daily email quota, or None if unlimited.
    """
    sent: int
    """
    The number of emails sent today.
    """
    received: int
    """
    The number of emails received today.
    """
    resets_at: str
    """
    When the daily quota resets, as an ISO 8601 datetime.
    """


class EmailsMonthlyUsage(TypedDict):
    """
    EmailsMonthlyUsage is the type that wraps the caller's monthly email usage.

    Attributes:
        used (int): The number of emails counted against the monthly quota
        limit (int): The monthly email quota
        sent (int): The number of emails sent this month
        received (int): The number of emails received this month
        resets_at (str): When the monthly quota resets, as an ISO 8601 datetime
    """

    used: int
    """
    The number of emails counted against the monthly quota.
    """
    limit: int
    """
    The monthly email quota.
    """
    sent: int
    """
    The number of emails sent this month.
    """
    received: int
    """
    The number of emails received this month.
    """
    resets_at: str
    """
    When the monthly quota resets, as an ISO 8601 datetime.
    """


class EmailsUsage(TypedDict):
    """
    EmailsUsage is the type that wraps the caller's email usage.

    Attributes:
        daily (EmailsDailyUsage): The caller's daily email usage
        monthly (EmailsMonthlyUsage): The caller's monthly email usage
    """

    daily: EmailsDailyUsage
    """
    The caller's daily email usage.
    """
    monthly: EmailsMonthlyUsage
    """
    The caller's monthly email usage.
    """


class ContactsUsage(TypedDict):
    """
    ContactsUsage is the type that wraps the caller's contacts usage.

    Attributes:
        used (int): The number of contacts counted against the quota
        limit (int): The contacts quota
    """

    used: int
    """
    The number of contacts counted against the quota.
    """
    limit: int
    """
    The contacts quota.
    """


class SegmentsUsage(TypedDict):
    """
    SegmentsUsage is the type that wraps the caller's segments usage.

    Attributes:
        used (int): The number of segments counted against the quota
        limit (Union[int, None]): The segments quota, or None if unlimited
    """

    used: int
    """
    The number of segments counted against the quota.
    """
    limit: Union[int, None]
    """
    The segments quota, or None if unlimited.
    """


class BroadcastsUsage(TypedDict):
    """
    BroadcastsUsage is the type that wraps the caller's broadcasts usage.

    Attributes:
        used (int): The number of broadcasts counted against the quota
        limit (None): The broadcasts quota, always None (unlimited)
    """

    used: int
    """
    The number of broadcasts counted against the quota.
    """
    limit: None
    """
    The broadcasts quota, always None (unlimited).
    """


class AiCreditsUsage(TypedDict):
    """
    AiCreditsUsage is the type that wraps the caller's AI credits usage.

    Attributes:
        used (int): The number of AI credits used
        limit (Union[int, None]): The AI credits quota, or None if unlimited
        next_increase_at (Union[str, None]): When the AI credits quota next \
        increases, as an ISO 8601 datetime, or None if not scheduled
    """

    used: int
    """
    The number of AI credits used.
    """
    limit: Union[int, None]
    """
    The AI credits quota, or None if unlimited.
    """
    next_increase_at: Union[str, None]
    """
    When the AI credits quota next increases, as an ISO 8601 datetime,
    or None if not scheduled.
    """


class AutomationRunsUsage(TypedDict):
    """
    AutomationRunsUsage is the type that wraps the caller's automation runs usage.

    Attributes:
        used (int): The number of automation runs counted against the quota
        limit (int): The automation runs quota
        resets_at (str): When the automation runs quota resets, as an ISO \
        8601 datetime
    """

    used: int
    """
    The number of automation runs counted against the quota.
    """
    limit: int
    """
    The automation runs quota.
    """
    resets_at: str
    """
    When the automation runs quota resets, as an ISO 8601 datetime.
    """


class DomainsUsage(TypedDict):
    """
    DomainsUsage is the type that wraps the caller's domains usage.

    Attributes:
        used (int): The number of domains counted against the quota
        limit (Union[int, None]): The domains quota, or None if unlimited
    """

    used: int
    """
    The number of domains counted against the quota.
    """
    limit: Union[int, None]
    """
    The domains quota, or None if unlimited.
    """


class RateLimitUsage(TypedDict):
    """
    RateLimitUsage is the type that wraps the caller's API rate limit.

    Attributes:
        limit (int): The number of requests allowed per duration window
        duration (str): The rate limit window (e.g. "1000ms")
    """

    limit: int
    """
    The number of requests allowed per duration window.
    """
    duration: str
    """
    The rate limit window (e.g. "1000ms").
    """


class Usage:

    class GetResponse(BaseResponse):
        """
        GetResponse type that wraps the caller's account-level usage and quota data

        Attributes:
            object (str): The object type, always "usage"
            emails (EmailsUsage): The caller's email usage
            contacts (ContactsUsage): The caller's contacts usage
            segments (SegmentsUsage): The caller's segments usage
            broadcasts (BroadcastsUsage): The caller's broadcasts usage
            ai_credits (AiCreditsUsage): The caller's AI credits usage
            automation_runs (AutomationRunsUsage): The caller's automation runs usage
            domains (DomainsUsage): The caller's domains usage
            rate_limit (RateLimitUsage): The caller's API rate limit
        """

        object: str
        """
        The object type, always "usage".
        """
        emails: EmailsUsage
        """
        The caller's email usage.
        """
        contacts: ContactsUsage
        """
        The caller's contacts usage.
        """
        segments: SegmentsUsage
        """
        The caller's segments usage.
        """
        broadcasts: BroadcastsUsage
        """
        The caller's broadcasts usage.
        """
        ai_credits: AiCreditsUsage
        """
        The caller's AI credits usage.
        """
        automation_runs: AutomationRunsUsage
        """
        The caller's automation runs usage.
        """
        domains: DomainsUsage
        """
        The caller's domains usage.
        """
        rate_limit: RateLimitUsage
        """
        The caller's API rate limit.
        """

    @classmethod
    def get(cls) -> GetResponse:
        """
        Retrieve the caller's account-level usage and quota data.
        see more: https://resend.com/docs/api-reference/usage/get-usage

        Returns:
            GetResponse: The usage object
        """
        path = "/usage"
        resp = request.Request[Usage.GetResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls) -> GetResponse:
        """
        Retrieve the caller's account-level usage and quota data (async).
        see more: https://resend.com/docs/api-reference/usage/get-usage

        Returns:
            GetResponse: The usage object
        """
        path = "/usage"
        resp = await AsyncRequest[Usage.GetResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp
