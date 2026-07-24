from typing import Any, Dict, List, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class BatchSuppression(TypedDict):
    """
    BatchSuppression is a single entry of a batch add response.

    Attributes:
        object (str): Always 'suppression'.
        id (str): The ID of the suppression.
    """

    object: str
    id: str


class BatchRemovedSuppression(TypedDict):
    """
    BatchRemovedSuppression is a single entry of a batch remove response.

    Attributes:
        object (str): Always 'suppression'.
        id (str): The ID of the removed suppression.
        deleted (bool): Whether the suppression was deleted.
    """

    object: str
    id: str
    deleted: bool


class SuppressionsBatch:
    class AddParams(TypedDict):
        emails: List[str]
        """
        The email addresses to suppress. Between 1 and 100 addresses.
        """

    class RemoveParams(TypedDict):
        emails: NotRequired[List[str]]
        """
        The email addresses to remove from the suppression list.
        Between 1 and 100 addresses. Cannot be used with the ids parameter.
        """
        ids: NotRequired[List[str]]
        """
        The suppression IDs to remove from the suppression list. Must be UUIDs.
        Between 1 and 100 IDs. Cannot be used with the emails parameter.
        """

    class AddResponse(BaseResponse):
        """
        AddResponse wraps the suppressions created by a batch add.

        Attributes:
            data (List[BatchSuppression]): The created suppressions.
        """

        data: List[BatchSuppression]

    class RemoveResponse(BaseResponse):
        """
        RemoveResponse wraps the suppressions removed by a batch remove.

        Attributes:
            data (List[BatchRemovedSuppression]): The removed suppressions.
        """

        data: List[BatchRemovedSuppression]

    # The API rejects `null` for the unset key, so RemoveParams uses NotRequired
    # (absent from the JSON body) rather than Optional, and the exclusivity the
    # server enforces is checked here since a TypedDict cannot express it. The
    # check and the body are built together so "None means absent" cannot drift
    # apart from what gets serialized.
    @staticmethod
    def _build_remove_body(
        params: "SuppressionsBatch.RemoveParams",
    ) -> Dict[str, Any]:
        has_emails = params.get("emails") is not None
        has_ids = params.get("ids") is not None
        if has_emails and has_ids:
            raise ValueError("emails and ids cannot be used together")
        if not has_emails and not has_ids:
            raise ValueError("emails or ids must be provided")
        return {key: value for key, value in params.items() if value is not None}

    @classmethod
    def add(cls, params: AddParams) -> AddResponse:
        """
        Add up to 100 email addresses to the suppression list at once. Addresses are
        normalized and deduplicated server-side, and already-suppressed addresses
        return their existing suppression rather than an error.
        see more: https://resend.com/docs/api-reference/suppressions/add-suppressions

        Args:
            params (AddParams): The batch add parameters

        Returns:
            AddResponse: The created suppressions. May contain fewer entries than
                emails sent, since duplicates collapse into one. Do not match
                entries to the emails you sent by index.
        """
        path = "/suppressions/batch/add"
        resp = request.Request[SuppressionsBatch.AddResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, params: RemoveParams) -> RemoveResponse:
        """
        Remove up to 100 suppressions at once, by email address or by ID.
        see more: https://resend.com/docs/api-reference/suppressions/remove-suppressions

        Args:
            params (RemoveParams): The batch remove parameters. Provide either
                emails or ids, but not both.

        Returns:
            RemoveResponse: The removed suppressions. Only identifiers that were
                actually suppressed are returned, so this may contain fewer entries
                than you sent - misses are omitted rather than reported as errors.
                Do not match entries to the identifiers you sent by index.
        """
        body = cls._build_remove_body(params)
        path = "/suppressions/batch/remove"
        resp = request.Request[SuppressionsBatch.RemoveResponse](
            path=path, params=body, verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def add_async(cls, params: AddParams) -> AddResponse:
        """
        Add up to 100 email addresses to the suppression list at once (async).
        Addresses are normalized and deduplicated server-side, and already-suppressed
        addresses return their existing suppression rather than an error.
        see more: https://resend.com/docs/api-reference/suppressions/add-suppressions

        Args:
            params (AddParams): The batch add parameters

        Returns:
            AddResponse: The created suppressions. May contain fewer entries than
                emails sent, since duplicates collapse into one. Do not match
                entries to the emails you sent by index.
        """
        path = "/suppressions/batch/add"
        resp = await AsyncRequest[SuppressionsBatch.AddResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, params: RemoveParams) -> RemoveResponse:
        """
        Remove up to 100 suppressions at once, by email address or by ID (async).
        see more: https://resend.com/docs/api-reference/suppressions/remove-suppressions

        Args:
            params (RemoveParams): The batch remove parameters. Provide either
                emails or ids, but not both.

        Returns:
            RemoveResponse: The removed suppressions. Only identifiers that were
                actually suppressed are returned, so this may contain fewer entries
                than you sent - misses are omitted rather than reported as errors.
                Do not match entries to the identifiers you sent by index.
        """
        body = cls._build_remove_body(params)
        path = "/suppressions/batch/remove"
        resp = await AsyncRequest[SuppressionsBatch.RemoveResponse](
            path=path, params=body, verb="post"
        ).perform_with_content()
        return resp
