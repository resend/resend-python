from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.logs._log import Log
from resend.pagination_helper import PaginationHelper

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class Logs:

    class GetResponse(BaseResponse):
        """
        GetResponse type that wraps a single log object

        Attributes:
            object (str): The object type, always "log"
            id (str): The log ID
            created_at (str): The date and time the log was created
            endpoint (str): The API endpoint that was called
            method (str): The HTTP method used
            response_status (int): The HTTP response status code
            user_agent (str): The user agent of the client
            request_body (Any): The original request body
            response_body (Any): The API response body
        """

        object: str
        """
        The object type, always "log"
        """
        id: str
        """
        The log ID
        """
        created_at: str
        """
        The date and time the log was created
        """
        endpoint: str
        """
        The API endpoint that was called
        """
        method: str
        """
        The HTTP method used
        """
        response_status: int
        """
        The HTTP response status code
        """
        user_agent: str
        """
        The user agent of the client
        """
        request_body: Any
        """
        The original request body
        """
        response_body: Any
        """
        The API response body
        """

    class ListResponse(BaseResponse):
        """
        ListResponse type that wraps a list of log objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[Log]): A list of log objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[Log]
        """
        A list of log objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of logs to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more logs (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more logs (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    @classmethod
    def get(cls, log_id: str) -> GetResponse:
        """
        Retrieve a single log by its ID.
        see more: https://resend.com/docs/api-reference/logs/retrieve-log

        Args:
            log_id (str): The ID of the log to retrieve

        Returns:
            GetResponse: The log object
        """
        path = f"/logs/{log_id}"
        resp = request.Request[Logs.GetResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of logs.
        see more: https://resend.com/docs/api-reference/logs/list-logs

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of logs to retrieve (max 100, min 1)
                - after: ID after which to retrieve more logs
                - before: ID before which to retrieve more logs

        Returns:
            ListResponse: A list of log objects
        """
        base_path = "/logs"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Logs.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, log_id: str) -> GetResponse:
        """
        Retrieve a single log by its ID (async).
        see more: https://resend.com/docs/api-reference/logs/retrieve-log

        Args:
            log_id (str): The ID of the log to retrieve

        Returns:
            GetResponse: The log object
        """
        path = f"/logs/{log_id}"
        resp = await AsyncRequest[Logs.GetResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of logs (async).
        see more: https://resend.com/docs/api-reference/logs/list-logs

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of logs to retrieve (max 100, min 1)
                - after: ID after which to retrieve more logs
                - before: ID before which to retrieve more logs

        Returns:
            ListResponse: A list of log objects
        """
        base_path = "/logs"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = await AsyncRequest[Logs.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp
