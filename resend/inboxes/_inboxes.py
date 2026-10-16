from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.inboxes._inbox import Inbox, InboxListItem
from resend.inboxes._query import inbox_path, without_keys
from resend.pagination_helper import PaginationHelper

from .agent._inbox_agent import InboxAgent
from .drafts._inbox_drafts import InboxDrafts
from .labels._inbox_labels import InboxLabels
from .threads._inbox_threads import InboxThreads

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class Inboxes:
    """
    Inboxes manages inboxes, which send and receive email at an address on one
    of your domains, and their agent settings, labels, threads and drafts.
    """

    class Agent(InboxAgent):
        pass

    class Labels(InboxLabels):
        pass

    class Threads(InboxThreads):
        pass

    class Drafts(InboxDrafts):
        pass

    class CreateParams(TypedDict):
        """
        CreateParams are the parameters for creating an inbox.

        Attributes:
            email_address (str): The inbox email address on one of your domains.
            name (NotRequired[str]): Internal name for the inbox.
            from_name (NotRequired[str]): The name recipients see when mail is sent from this inbox.
            forwarding (NotRequired[bool]): Provision a receiving address instead of an MX record.
        """

        email_address: str
        """
        The inbox email address on one of your domains. The API trims and
        lowercases it. The part before the ``@`` is at most 64 characters and
        contains only letters, numbers, and ``. _ % + -``. It cannot start or end
        with a dot or contain two dots in a row.
        """
        name: NotRequired[str]
        """
        Internal name for the inbox. Recipients do not see it. Max 64 characters.
        Defaults to ``email_address``.
        """
        from_name: NotRequired[str]
        """
        The name recipients see when mail is sent from this inbox. A plain name,
        not a ``Name <email>`` address. Max 78 characters. It cannot contain a
        colon, ``<``, ``>``, line breaks, or other control characters. An email
        address inside the name must be on a domain the team has verified for
        sending. An empty string leaves it unset.
        """
        forwarding: NotRequired[bool]
        """
        When True, Resend provisions a receiving address so you can receive mail
        without adding an MX record. The address is returned in ``receiving_address``.
        Defaults to False.
        """

    class CreateResponse(BaseResponse):
        """
        CreateResponse is the response of creating an inbox.

        Attributes:
            object (str): The object type, always "inbox"
            id (str): The ID of the inbox
        """

        object: str
        """
        The object type, always "inbox".
        """
        id: str
        """
        The ID of the inbox.
        """

    class ListParams(TypedDict):
        """
        ListParams are the pagination parameters for listing inboxes.

        Attributes:
            limit (NotRequired[int]): Number of inboxes to retrieve. Maximum is 100, minimum is 1.
            after (NotRequired[str]): The ID after which to retrieve more inboxes.
            before (NotRequired[str]): The ID before which to retrieve more inboxes.
        """

        limit: NotRequired[int]
        """
        Number of inboxes to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more inboxes (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more inboxes (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is a page of the inboxes of the team.

        Attributes:
            object (str): The object type, always "list"
            has_more (bool): Whether there are more results available
            data (List[InboxListItem]): The inboxes, newest first
        """

        object: str
        """
        The object type, always "list".
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """
        data: List[InboxListItem]
        """
        The inboxes on this page, newest first.
        """

    class UpdateParams(TypedDict):
        """
        UpdateParams are the parameters for updating an inbox.
        Provide at least one of ``name`` or ``from_name``.

        Attributes:
            id (str): The Inbox ID or the inbox email address.
            name (NotRequired[str]): New internal name for the inbox.
            from_name (NotRequired[str]): The name recipients see when mail is sent from this inbox.
        """

        id: str
        """
        The Inbox ID or the inbox email address.
        """
        name: NotRequired[str]
        """
        New internal name for the inbox. Recipients do not see it.
        Between 1 and 64 characters after trimming.
        """
        from_name: NotRequired[str]
        """
        The name recipients see when mail is sent from this inbox. A plain name,
        not a ``Name <email>`` address. Max 78 characters. It cannot contain a
        colon, ``<``, ``>``, line breaks, or other control characters. An email
        address inside the name must be on a domain the team has verified for
        sending. An empty string removes it.
        """

    class UpdateResponse(BaseResponse):
        """
        UpdateResponse is the response of updating an inbox.

        Attributes:
            object (str): The object type, always "inbox"
            id (str): The ID of the inbox
        """

        object: str
        """
        The object type, always "inbox".
        """
        id: str
        """
        The ID of the inbox.
        """

    class RemoveResponse(BaseResponse):
        """
        RemoveResponse is the response of removing an inbox.

        Attributes:
            object (str): The object type, always "inbox"
            id (str): The ID of the inbox
            deleted (bool): Whether the inbox was deleted
        """

        object: str
        """
        The object type, always "inbox".
        """
        id: str
        """
        The ID of the inbox.
        """
        deleted: bool
        """
        Indicates whether the inbox was successfully deleted.
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateResponse:
        """
        Create an inbox that sends and receives email at an address on one of your
        domains. The domain must belong to the team. Without ``forwarding``, the
        domain must have receiving enabled, with DKIM and SPF verified and the
        inbound MX record verified or pending. With ``forwarding`` set to True, the
        domain only needs DKIM and SPF verified for sending, and Resend generates a
        ``receiving_address`` on the team inbound domain. A domain that does not
        meet these rules returns a 422 validation_error. An address or receiving
        address that is already in use returns a 409. A team that has reached the
        inbox limit of its plan returns a 403 validation_error. A blocked account
        returns a 451.
        see more: https://resend.com/docs/api-reference/inboxes/create-inbox

        Args:
            params (CreateParams): The inbox parameters

        Returns:
            CreateResponse: The object type and the ID of the inbox
        """
        path = "/inboxes"
        resp = request.Request[Inboxes.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve the inboxes of the team, newest first. The list items carry fewer
        fields than a single inbox. Retrieve an inbox to get all its fields. The
        ``after`` and ``before`` cursors take an inbox ID. A value that is not a
        UUID returns a 422, and an unknown ID returns a 404.
        see more: https://resend.com/docs/api-reference/inboxes/list-inboxes

        Args:
            params (Optional[ListParams]): Optional pagination parameters

        Returns:
            ListResponse: A page of the inboxes of the team
        """
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path("/inboxes", query_params)
        resp = request.Request[Inboxes.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, inbox_id: str) -> Inbox:
        """
        Retrieve a single inbox by ID or email address.
        see more: https://resend.com/docs/api-reference/inboxes/get-inbox

        Args:
            inbox_id (str): The Inbox ID or the inbox email address, such as
                ``support@acme.com``. A value that contains ``@`` must be a valid
                email address, and the match is case-insensitive. Any other value
                must be a UUID.

        Returns:
            Inbox: The inbox object
        """
        path = inbox_path(inbox_id)
        resp = request.Request[Inbox](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update the internal name of an inbox or the name recipients see when mail
        is sent from it. At least one of ``name`` or ``from_name`` is required.
        see more: https://resend.com/docs/api-reference/inboxes/update-inbox

        Args:
            params (UpdateParams): The inbox ID and the fields to change

        Returns:
            UpdateResponse: The object type and the ID of the inbox
        """
        path = inbox_path(params["id"])
        resp = request.Request[Inboxes.UpdateResponse](
            path=path, params=without_keys(params, "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, inbox_id: str) -> RemoveResponse:
        """
        Remove an inbox. An inbox that does not exist or was already removed
        returns a 404 not_found.
        see more: https://resend.com/docs/api-reference/inboxes/delete-inbox

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.

        Returns:
            RemoveResponse: The inbox ID and its deleted status
        """
        path = inbox_path(inbox_id)
        resp = request.Request[Inboxes.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(cls, params: CreateParams) -> CreateResponse:
        """
        Create an inbox that sends and receives email at an address on one of your
        domains (async). The domain must belong to the team. Without ``forwarding``,
        the domain must have receiving enabled, with DKIM and SPF verified and the
        inbound MX record verified or pending. With ``forwarding`` set to True, the
        domain only needs DKIM and SPF verified for sending, and Resend generates a
        ``receiving_address`` on the team inbound domain. A domain that does not
        meet these rules returns a 422 validation_error. An address or receiving
        address that is already in use returns a 409. A team that has reached the
        inbox limit of its plan returns a 403 validation_error. A blocked account
        returns a 451.
        see more: https://resend.com/docs/api-reference/inboxes/create-inbox

        Args:
            params (CreateParams): The inbox parameters

        Returns:
            CreateResponse: The object type and the ID of the inbox
        """
        path = "/inboxes"
        resp = await AsyncRequest[Inboxes.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve the inboxes of the team, newest first (async). The list items
        carry fewer fields than a single inbox. Retrieve an inbox to get all its
        fields. The ``after`` and ``before`` cursors take an inbox ID. A value that
        is not a UUID returns a 422, and an unknown ID returns a 404.
        see more: https://resend.com/docs/api-reference/inboxes/list-inboxes

        Args:
            params (Optional[ListParams]): Optional pagination parameters

        Returns:
            ListResponse: A page of the inboxes of the team
        """
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path("/inboxes", query_params)
        resp = await AsyncRequest[Inboxes.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, inbox_id: str) -> Inbox:
        """
        Retrieve a single inbox by ID or email address (async).
        see more: https://resend.com/docs/api-reference/inboxes/get-inbox

        Args:
            inbox_id (str): The Inbox ID or the inbox email address, such as
                ``support@acme.com``. A value that contains ``@`` must be a valid
                email address, and the match is case-insensitive. Any other value
                must be a UUID.

        Returns:
            Inbox: The inbox object
        """
        path = inbox_path(inbox_id)
        resp = await AsyncRequest[Inbox](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update the internal name of an inbox or the name recipients see when mail
        is sent from it (async). At least one of ``name`` or ``from_name`` is required.
        see more: https://resend.com/docs/api-reference/inboxes/update-inbox

        Args:
            params (UpdateParams): The inbox ID and the fields to change

        Returns:
            UpdateResponse: The object type and the ID of the inbox
        """
        path = inbox_path(params["id"])
        resp = await AsyncRequest[Inboxes.UpdateResponse](
            path=path, params=without_keys(params, "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, inbox_id: str) -> RemoveResponse:
        """
        Remove an inbox (async). An inbox that does not exist or was already
        removed returns a 404 not_found.
        see more: https://resend.com/docs/api-reference/inboxes/delete-inbox

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.

        Returns:
            RemoveResponse: The inbox ID and its deleted status
        """
        path = inbox_path(inbox_id)
        resp = await AsyncRequest[Inboxes.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
