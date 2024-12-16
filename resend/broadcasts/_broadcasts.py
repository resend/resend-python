from typing import Any, Dict, List, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request

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


class _CreateResponse(TypedDict):
    id: str
    """
    id of the created broadcast
    """


class _SendResponse(_CreateResponse):
    pass


class _RemoveResponse(TypedDict):
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


class _ListResponse(TypedDict):
    object: str
    """
    object type: "list"
    """
    data: List[Broadcast]
    """
    A list of broadcast objects
    """


class _CreateParamsDefault(_CreateParamsFrom):
    audience_id: str
    """
    The ID of the audience you want to send to.
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


class _SendBroadcastParams(TypedDict):
    broadcast_id: str
    """
    The ID of the broadcast to send.
    """
    scheduled_at: NotRequired[str]
    """
    Schedule email to be sent later.
    The date should be in natural language (e.g.: in 1 min) or ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
    """


class Broadcasts:

    class CreateParams(_CreateParamsDefault):
        """CreateParams is the class that wraps the parameters for the create method.

        Attributes:
            from (str): The sender email address
            audience_id (str): The ID of the audience you want to send to.
            subject (str): Email subject.
            reply_to (NotRequired[Union[List[str], str]]): Reply-to email address(es).
            html (NotRequired[str]): The HTML version of the message.
            text (NotRequired[str]): The text version of the message.
            name (NotRequired[str]): The friendly name of the broadcast. Only used for internal reference.
        """

    class SendParams(_SendBroadcastParams):
        """SendParams is the class that wraps the parameters for the send method.

        Attributes:
            broadcast_id (str): The ID of the broadcast to send.
            scheduled_at (NotRequired[str]): Schedule email to be sent later.
            The date should be in language natural (e.g.: in 1 min) or ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
        """

    class CreateResponse(_CreateResponse):
        """
        CreateResponse is the class that wraps the response of the create method.

        Attributes:
            id (str): id of the created broadcast
        """

    class SendResponse(_SendResponse):
        """
        SendResponse is the class that wraps the response of the send method.

        Attributes:
            id (str): id of the created broadcast
        """

    class ListResponse(_ListResponse):
        """
        ListResponse is the class that wraps the response of the list method.

        Attributes:
            object (str): object type: "list"
            data (List[Broadcast]): A list of broadcast objects
        """

    class RemoveResponse(_RemoveResponse):
        """
        RemoveResponse is the class that wraps the response of the remove method.

        Attributes:
            object (str): object type: "broadcast"
            id (str): id of the removed broadcast
            deleted (bool): True if the broadcast was deleted
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
        resp = request.Request[_CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def send(cls, params: SendParams) -> SendResponse:
        """
        Sends a broadcast.
        see more: https://resend.com/docs/api-reference/broadcasts/send-broadcast

        Args:
            params (CreateParams): The audience creation parameters

        Returns:
            SendResponse: The new broadcast object response
        """
        path = f"/broadcasts/{params['broadcast_id']}/send"
        resp = request.Request[_SendResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls) -> ListResponse:
        """
        Retrieve a list of broadcasts.
        see more: https://resend.com/docs/api-reference/broadcasts/list-broadcasts

        Returns:
            ListResponse: A list of broadcast objects
        """
        path = "/broadcasts/"
        resp = request.Request[_ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str) -> Broadcast:
        """
        Retrieve a single broadcast.
        see more: https://resend.com/docs/api-reference/broadcasts/get-broadcast

        Args:
            id (str): The audience ID

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
        resp = request.Request[_RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
