from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import quote

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper

from ._event import Event, EventListItem, EventSchema

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class Events:

    class CreateParams(TypedDict):
        """
        CreateParams is the class that wraps the parameters for the create method.

        Attributes:
            name (str): The name of the event. Cannot start with the "resend:" prefix.
            schema (NotRequired[Union[EventSchema, None]]): Flat key/type map defining the payload schema.
        """

        name: str
        """
        The name of the event. Cannot start with the "resend:" prefix.
        """
        schema: NotRequired[Union[EventSchema, None]]
        """
        Flat key/type map defining the event payload schema.
        Supported types: "string", "number", "boolean", "date".
        """

    class UpdateParams(TypedDict):
        """
        UpdateParams is the class that wraps the parameters for the update method.

        Attributes:
            identifier (str): The event ID (UUID) or event name.
            schema (Union[EventSchema, None]): Updated schema. Set to None to clear the schema.
        """

        identifier: str
        """
        The event ID (UUID) or event name.
        """
        schema: Union[EventSchema, None]
        """
        Updated schema definition. Set to None to clear the schema.
        Supported types: "string", "number", "boolean", "date".
        """

    class SendParams(TypedDict):
        """
        SendParams is the class that wraps the parameters for the send method.
        Exactly one of contact_id or email must be provided.

        Attributes:
            event (str): The name of the event to send.
            contact_id (NotRequired[str]): The contact ID to send the event for.
            email (NotRequired[str]): The email address to send the event for.
            payload (NotRequired[Dict[str, Any]]): Key/value pairs to include with the event.
        """

        event: str
        """
        The name of the event to send.
        """
        contact_id: NotRequired[str]
        """
        The contact ID to send the event for.
        Exactly one of contact_id or email must be provided.
        """
        email: NotRequired[str]
        """
        The email address to send the event for.
        Exactly one of contact_id or email must be provided.
        """
        payload: NotRequired[Dict[str, Any]]
        """
        Key/value pairs to include with the event.
        """

    class ListParams(TypedDict):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            limit (NotRequired[int]): Number of events to retrieve (max 100, min 1)
            after (NotRequired[str]): Return items after this cursor
            before (NotRequired[str]): Return items before this cursor
        """

        limit: NotRequired[int]
        """
        Number of events to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        Return items after this cursor (for pagination).
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        Return items before this cursor (for pagination).
        Cannot be used with the after parameter.
        """

    class CreateResponse(BaseResponse):
        """
        CreateResponse is the class that wraps the response of the create method.

        Attributes:
            object (str): The object type, always "event"
            id (str): The ID of the created event
        """

        object: str
        """
        The object type, always "event".
        """
        id: str
        """
        The ID of the created event (UUID).
        """

    class UpdateResponse(BaseResponse):
        """
        UpdateResponse is the class that wraps the response of the update method.

        Attributes:
            object (str): The object type, always "event"
            id (str): The ID of the updated event
        """

        object: str
        """
        The object type, always "event".
        """
        id: str
        """
        The ID of the updated event (UUID).
        """

    class DeleteResponse(BaseResponse):
        """
        DeleteResponse is the class that wraps the response of the remove method.

        Attributes:
            object (str): The object type, always "event"
            id (str): The ID of the deleted event
            deleted (bool): Whether the event was successfully deleted
        """

        object: str
        """
        The object type, always "event".
        """
        id: str
        """
        The ID of the deleted event (UUID).
        """
        deleted: bool
        """
        Whether the event was successfully deleted.
        """

    class SendResponse(BaseResponse):
        """
        SendResponse is the class that wraps the response of the send method.

        Attributes:
            object (str): The object type, always "event"
            event (str): The name of the event that was sent
        """

        object: str
        """
        The object type, always "event".
        """
        event: str
        """
        The name of the event that was sent.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is the class that wraps the response of the list method.

        Attributes:
            object (str): The object type, always "list"
            data (List[EventListItem]): A list of event objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list".
        """
        data: List[EventListItem]
        """
        A list of event objects.
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """

    @classmethod
    def create(cls, params: "Events.CreateParams") -> "Events.CreateResponse":
        """
        Create an event definition.
        see more: https://resend.com/docs/api-reference/events/create-event

        Args:
            params (CreateParams): The event creation parameters

        Returns:
            CreateResponse: The created event response
        """
        path = "/events"
        resp = request.Request[Events.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, identifier: str) -> Event:
        """
        Retrieve a single event by ID or name.
        see more: https://resend.com/docs/api-reference/events/get-event

        Args:
            identifier (str): The event ID (UUID) or event name

        Returns:
            Event: The event object
        """
        path = f"/events/{quote(identifier, safe='')}"
        resp = request.Request[Event](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: "Events.UpdateParams") -> "Events.UpdateResponse":
        """
        Update an event definition.
        see more: https://resend.com/docs/api-reference/events/update-event

        Args:
            params (UpdateParams): The event update parameters

        Returns:
            UpdateResponse: The updated event response
        """
        path = f"/events/{quote(params['identifier'], safe='')}"
        body = {k: v for k, v in params.items() if k != "identifier"}
        resp = request.Request[Events.UpdateResponse](
            path=path, params=cast(Dict[Any, Any], body), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, identifier: str) -> "Events.DeleteResponse":
        """
        Delete an event definition.
        see more: https://resend.com/docs/api-reference/events/delete-event

        Args:
            identifier (str): The event ID (UUID) or event name

        Returns:
            DeleteResponse: The delete response
        """
        path = f"/events/{quote(identifier, safe='')}"
        resp = request.Request[Events.DeleteResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    def send(cls, params: "Events.SendParams") -> "Events.SendResponse":
        """
        Send an event for a contact.
        see more: https://resend.com/docs/api-reference/events/send-event

        Args:
            params (SendParams): The event send parameters.
                Exactly one of contact_id or email must be provided.

        Returns:
            SendResponse: The send event response
        """
        path = "/events/send"
        resp = request.Request[Events.SendResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(
        cls, params: Optional["Events.ListParams"] = None
    ) -> "Events.ListResponse":
        """
        Retrieve a list of event definitions.
        see more: https://resend.com/docs/api-reference/events/list-events

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of events to retrieve (max 100, min 1)
                - after: Return items after this cursor
                - before: Return items before this cursor

        Returns:
            ListResponse: A list of event objects
        """
        base_path = "/events"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Events.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(
        cls, params: "Events.CreateParams"
    ) -> "Events.CreateResponse":
        """
        Create an event definition (async).
        see more: https://resend.com/docs/api-reference/events/create-event

        Args:
            params (CreateParams): The event creation parameters

        Returns:
            CreateResponse: The created event response
        """
        path = "/events"
        resp = await AsyncRequest[Events.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, identifier: str) -> Event:
        """
        Retrieve a single event by ID or name (async).
        see more: https://resend.com/docs/api-reference/events/get-event

        Args:
            identifier (str): The event ID (UUID) or event name

        Returns:
            Event: The event object
        """
        path = f"/events/{quote(identifier, safe='')}"
        resp = await AsyncRequest[Event](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(
        cls, params: "Events.UpdateParams"
    ) -> "Events.UpdateResponse":
        """
        Update an event definition (async).
        see more: https://resend.com/docs/api-reference/events/update-event

        Args:
            params (UpdateParams): The event update parameters

        Returns:
            UpdateResponse: The updated event response
        """
        path = f"/events/{quote(params['identifier'], safe='')}"
        body = {k: v for k, v in params.items() if k != "identifier"}
        resp = await AsyncRequest[Events.UpdateResponse](
            path=path, params=cast(Dict[Any, Any], body), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, identifier: str) -> "Events.DeleteResponse":
        """
        Delete an event definition (async).
        see more: https://resend.com/docs/api-reference/events/delete-event

        Args:
            identifier (str): The event ID (UUID) or event name

        Returns:
            DeleteResponse: The delete response
        """
        path = f"/events/{quote(identifier, safe='')}"
        resp = await AsyncRequest[Events.DeleteResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def send_async(cls, params: "Events.SendParams") -> "Events.SendResponse":
        """
        Send an event for a contact (async).
        see more: https://resend.com/docs/api-reference/events/send-event

        Args:
            params (SendParams): The event send parameters.
                Exactly one of contact_id or email must be provided.

        Returns:
            SendResponse: The send event response
        """
        path = "/events/send"
        resp = await AsyncRequest[Events.SendResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(
        cls, params: Optional["Events.ListParams"] = None
    ) -> "Events.ListResponse":
        """
        Retrieve a list of event definitions (async).
        see more: https://resend.com/docs/api-reference/events/list-events

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of events to retrieve (max 100, min 1)
                - after: Return items after this cursor
                - before: Return items before this cursor

        Returns:
            ListResponse: A list of event objects
        """
        base_path = "/events"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = await AsyncRequest[Events.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp
