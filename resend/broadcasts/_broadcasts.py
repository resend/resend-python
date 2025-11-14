from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper

from ._broadcast import Broadcast

# _CreateParamsFrom is declared with functional TypedDict syntax here because
# "from" is a reserved keyword in Python, and this is the best way to
# support type-checking for it.
_CreateParamsFrom = TypedDict(
    "_CreateParamsFrom",
    {
        "from": str,
    },
)

_UpdateParamsFrom = TypedDict(
    "_UpdateParamsFrom",
    {
        "from": NotRequired[str],
    },
)


class Broadcasts:

    class CreateParams(_CreateParamsFrom):
        """CreateParams is the class that wraps the parameters for the create method.

        Attributes:
            from (str): The sender email address
            segment_id (NotRequired[str]): The ID of the segment you want to send to.
            audience_id (NotRequired[str]): The ID of the audience you want to send to. (deprecated: use segment_id)
            subject (str): Email subject.
            reply_to (NotRequired[Union[List[str], str]]): Reply-to email address(es).
            html (NotRequired[str]): The HTML version of the message.
            text (NotRequired[str]): The text version of the message.
            name (NotRequired[str]): The friendly name of the broadcast. Only used for internal reference.
        """

        segment_id: NotRequired[str]
        """
        The ID of the segment you want to send to.
        """
        audience_id: NotRequired[str]
        """
        The ID of the audience you want to send to.

        .. deprecated::
            Use segment_id instead.
        """
        subject: str
        """
        Email subject.
        """
        reply_to: NotRequired[Union[List[str], str]]
        """
        Reply-to email address. For multiple addresses, send as an array of strings.
        """
        html: NotRequired[str]
        """
        The HTML version of the message.
        """
        text: NotRequired[str]
        """
        The text version of the message.
        """
        name: NotRequired[str]
        """
        The friendly name of the broadcast. Only used for internal reference.
        """

    class UpdateParams(_UpdateParamsFrom):
        """UpdateParams is the class that wraps the parameters for the update method.

        Attributes:
            broadcast_id (str): The ID of the broadcast you want to update.
            segment_id (NotRequired[str]): The ID of the segment you want to send to.
            audience_id (NotRequired[str]): The ID of the audience you want to send to. (deprecated: use segment_id)
            from (NotRequired[str]): The sender email address
            subject (NotRequired[str]): Email subject.
            reply_to (NotRequired[Union[List[str], str]]): Reply-to email address(es).
            html (NotRequired[str]): The HTML version of the message.
            text (NotRequired[str]): The text version of the message.
            name (NotRequired[str]): The friendly name of the broadcast. Only used for internal reference.
        """

        broadcast_id: str
        """
        The ID of the broadcast you want to update.
        """
        segment_id: NotRequired[str]
        """
        The ID of the segment you want to send to.
        """
        audience_id: NotRequired[str]
        """
        The ID of the audience you want to send to.

        .. deprecated::
            Use segment_id instead.
        """
        subject: NotRequired[str]
        """
        Email subject.
        """
        reply_to: NotRequired[Union[List[str], str]]
        """
        Reply-to email address. For multiple addresses, send as an array of strings.
        """
        html: NotRequired[str]
        """
        The HTML version of the message.
        """
        text: NotRequired[str]
        """
        The text version of the message.
        """
        name: NotRequired[str]
        """
        The friendly name of the broadcast. Only used for internal reference.
        """

    class SendParams(TypedDict):
        """SendParams is the class that wraps the parameters for the send method.

        Attributes:
            broadcast_id (str): The ID of the broadcast to send.
            scheduled_at (NotRequired[str]): Schedule email to be sent later.
            The date should be in natural language (e.g.: in 1 min) or ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
        """

        broadcast_id: str
        """
        The ID of the broadcast to send.
        """
        scheduled_at: NotRequired[str]
        """
        Schedule email to be sent later.
        The date should be in natural language (e.g.: in 1 min) or ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
        """

    class CreateResponse(BaseResponse):
        """
        CreateResponse is the class that wraps the response of the create method.

        Attributes:
            id (str): id of the created broadcast
        """

        id: str
        """
        id of the created broadcast
        """

    class UpdateResponse(BaseResponse):
        """
        UpdateResponse is the class that wraps the response of the update method.

        Attributes:
            id (str): id of the updated broadcast
        """

        id: str
        """
        id of the updated broadcast
        """

    class SendResponse(CreateResponse):
        """
        SendResponse is the class that wraps the response of the send method.

        Attributes:
            id (str): id of the created broadcast
        """

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of broadcasts to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more broadcasts (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more broadcasts (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is the class that wraps the response of the list method with pagination metadata.

        Attributes:
            object (str): object type, always "list"
            data (List[Broadcast]): A list of broadcast objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        object type, always "list"
        """
        data: List[Broadcast]
        """
        A list of broadcast objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class RemoveResponse(BaseResponse):
        """
        RemoveResponse is the class that wraps the response of the remove method.

        Attributes:
            object (str): object type: "broadcast"
            id (str): id of the removed broadcast
            deleted (bool): True if the broadcast was deleted
        """

        object: str
        """
        object type: "broadcast"
        """
        id: str
        """
        id of the removed broadcast
        """
        deleted: bool
        """
        True if the broadcast was deleted
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateResponse:
        """
        Create a broadcast.
        see more: https://resend.com/docs/api-reference/broadcasts/create-broadcast

        Args:
            params (CreateParams): The broadcast creation parameters

        Returns:
            CreateResponse: The new broadcast object response
        """

        path = "/broadcasts"
        resp = request.Request[Broadcasts.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update a broadcast.
        see more: https://resend.com/docs/api-reference/broadcasts/update-broadcast

        Args:
            params (UpdateParams): The broadcast update parameters

        Returns:
            UpdateResponse: The updated broadcast object response
        """

        path = f"/broadcasts/{params['broadcast_id']}"
        resp = request.Request[Broadcasts.UpdateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def send(cls, params: SendParams) -> SendResponse:
        """
        Sends a broadcast.
        see more: https://resend.com/docs/api-reference/broadcasts/send-broadcast

        Args:
            params (CreateParams): The broadcast creation parameters

        Returns:
            SendResponse: The new broadcast object response
        """

        path = f"/broadcasts/{params['broadcast_id']}/send"
        resp = request.Request[Broadcasts.SendResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of broadcasts.
        see more: https://resend.com/docs/api-reference/broadcasts/list-broadcasts

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of broadcasts to retrieve (max 100, min 1).
                  If not provided, all broadcasts will be returned without pagination.
                - after: ID after which to retrieve more broadcasts
                - before: ID before which to retrieve more broadcasts

        Returns:
            ListResponse: A list of broadcast objects
        """
        base_path = "/broadcasts"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Broadcasts.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str) -> Broadcast:
        """
        Retrieve a single broadcast.
        see more: https://resend.com/docs/api-reference/broadcasts/get-broadcast

        Args:
            id (str): The broadcast ID

        Returns:
            Broadcast: The broadcast object
        """
        path = f"/broadcasts/{id}"
        resp = request.Request[Broadcast](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, id: str) -> RemoveResponse:
        """
        Delete a single broadcast.
        see more: https://resend.com/docs/api-reference/broadcasts/delete-broadcasts

        Args:
            id (str): The broadcast ID

        Returns:
            RemoveResponse: The remove response object
        """
        path = f"/broadcasts/{id}"
        resp = request.Request[Broadcasts.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
