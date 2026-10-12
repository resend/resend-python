from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.inboxes._inbox import InboxMessageFolder, MoveThreadFolder
from resend.inboxes._query import build_inbox_query_path, without_keys

from ._inbox_thread import (InboxThread, InboxThreadSearchResult,
                            InboxThreadSummary)
from .emails._inbox_thread_emails import InboxThreadEmails

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class _ListParams(TypedDict):
    folders: NotRequired[List[InboxMessageFolder]]
    """
    Folders to list, for example ``["inbox", "sent"]``. A thread is returned when
    any of its emails is in one of the folders, so a thread in ``inbox`` with an
    email you sent matches both ``inbox`` and ``sent``. Defaults to ``inbox``, or
    to ``inbox,archive,sent`` when ``labels`` is set. ``spam`` and ``trash`` are
    only included when you name them.
    """
    labels: NotRequired[List[str]]
    """
    Label IDs. Returns threads with any of these labels. Up to 50 IDs.
    An ID that does not exist in the inbox returns a 404.
    """
    read: NotRequired[bool]
    """
    True returns threads where every email is read. False returns threads with
    at least one unread email.
    """
    limit: NotRequired[int]
    """
    Number of threads to retrieve. Maximum is 100, and minimum is 1.
    """
    after: NotRequired[str]
    """
    The thread ID after which we'll retrieve more threads (for pagination).
    Cannot be used with the before parameter.
    """
    before: NotRequired[str]
    """
    The thread ID before which we'll retrieve more threads (for pagination).
    Cannot be used with the after parameter.
    """


# Functional syntax required because ``from`` is a reserved keyword.
_SearchParamsFrom = TypedDict(
    "_SearchParamsFrom",
    {
        "from": NotRequired[List[str]],
    },
)


class _SearchParams(_ListParams, _SearchParamsFrom):
    query: NotRequired[str]
    """
    Free text to search for in the subject, body, sender, recipients, and
    attachment names. Every word must match. Wrap words in double quotes to match
    an exact phrase. Start a word or quoted phrase with ``-`` to exclude it.
    Max 256 characters and 32 words.
    """
    to: NotRequired[List[str]]
    """
    Recipients, matched the same way as ``from``. Up to 20 values.
    """
    cc: NotRequired[List[str]]
    """
    CC recipients, matched the same way as ``from``. Up to 20 values.
    """
    bcc: NotRequired[List[str]]
    """
    BCC recipients, matched the same way as ``from``. Up to 20 values.
    """
    has_attachment: NotRequired[bool]
    """
    True matches emails with an attachment. False matches emails without one.
    """
    start_date: NotRequired[str]
    """
    Matches emails sent on or after this date. Accepts a date like ``2026-09-01``
    or an ISO 8601 timestamp, in UTC unless the timestamp has an offset.
    """
    end_date: NotRequired[str]
    """
    Matches emails sent on or before this date. Same formats as ``start_date``.
    A date covers that whole day. A timestamp is used as given. An ``end_date``
    before ``start_date`` returns a 422 validation_error.
    """


class InboxThreads:
    """
    InboxThreads manages the threads of an inbox. A thread is a conversation
    made up of one or more emails.
    """

    class Emails(InboxThreadEmails):
        pass

    class ListParams(_ListParams):
        """
        ListParams are the filter and pagination parameters for listing threads.

        Attributes:
            folders (NotRequired[List[InboxMessageFolder]]): Folders to list.
            labels (NotRequired[List[str]]): Label IDs. Returns threads with any of these labels.
            read (NotRequired[bool]): Filter by read state.
            limit (NotRequired[int]): Number of threads to retrieve. Maximum is 100, minimum is 1.
            after (NotRequired[str]): The thread ID after which to retrieve more threads.
            before (NotRequired[str]): The thread ID before which to retrieve more threads.
        """

    class SearchParams(_SearchParams):
        """
        SearchParams are the search, filter and pagination parameters for searching
        threads. Different parameters combine, so a thread must match all of them.
        ``folders``, ``labels``, and ``read`` apply to the thread. ``query``,
        ``from``, ``to``, ``cc``, ``bcc``, ``has_attachment``, ``start_date``, and
        ``end_date`` must all match the same email in the thread.

        Attributes:
            query (NotRequired[str]): Free text to search for.
            from (NotRequired[List[str]]): Senders. Each value matches part of the
                sender's address or name, without case. Up to 20 values.
            to (NotRequired[List[str]]): Recipients.
            cc (NotRequired[List[str]]): CC recipients.
            bcc (NotRequired[List[str]]): BCC recipients.
            has_attachment (NotRequired[bool]): Filter by attachment.
            start_date (NotRequired[str]): Matches emails sent on or after this date.
            end_date (NotRequired[str]): Matches emails sent on or before this date.
            folders (NotRequired[List[InboxMessageFolder]]): Folders to search.
            labels (NotRequired[List[str]]): Label IDs.
            read (NotRequired[bool]): Filter by read state.
            limit (NotRequired[int]): Number of threads to retrieve.
            after (NotRequired[str]): The thread ID after which to retrieve more threads.
            before (NotRequired[str]): The thread ID before which to retrieve more threads.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is a page of the threads of an inbox.

        Attributes:
            object (str): The object type, always "list"
            has_more (bool): Whether there are more results available
            data (List[InboxThread]): The matching threads, most recently active first
        """

        object: str
        """
        The object type, always "list".
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """
        data: List[InboxThread]
        """
        The matching threads, most recently active first.
        """

    class SearchResponse(BaseResponse):
        """
        SearchResponse is a page of the threads that match a search.

        Attributes:
            object (str): The object type, always "list"
            has_more (bool): Whether there are more results available
            data (List[InboxThreadSearchResult]): The matching threads, most recently active first
        """

        object: str
        """
        The object type, always "list".
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """
        data: List[InboxThreadSearchResult]
        """
        The matching threads, most recently active first.
        """

    class UpdateParams(TypedDict):
        """
        UpdateParams are the parameters for updating a thread. At least one of
        ``read``, ``folder``, ``label_id``, ``add_label_ids``, or ``remove_label_ids``
        is required. A label ID cannot be both added and removed in the same request.

        Attributes:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            id (str): The Thread ID.
            read (NotRequired[bool]): Marks every email in the thread read or unread.
            folder (NotRequired[MoveThreadFolder]): Moves the thread to this folder.
            label_id (NotRequired[str]): Deprecated. Use add_label_ids instead.
            add_label_ids (NotRequired[List[str]]): Label IDs to apply to the thread.
            remove_label_ids (NotRequired[List[str]]): Label IDs to remove from the thread.
        """

        inbox_id: str
        """
        The Inbox ID. An email address is not accepted.
        """
        id: str
        """
        The Thread ID.
        """
        read: NotRequired[bool]
        """
        Marks every email in the thread read or unread.
        """
        folder: NotRequired[MoveThreadFolder]
        """
        Moves the thread to this folder. ``sent`` is assigned automatically and
        cannot be set. Moving a thread out of ``trash`` restores it and clears its
        deletion deadline.
        """
        label_id: NotRequired[str]
        """
        Deprecated. Use ``add_label_ids`` instead. Applies this label to the
        thread, the same as one entry in ``add_label_ids``. A label ID that does
        not exist in the inbox returns a 404.
        """
        add_label_ids: NotRequired[List[str]]
        """
        Label IDs to apply to the thread. Between 1 and 10 IDs.
        A label ID that does not exist in the inbox returns a 404.
        """
        remove_label_ids: NotRequired[List[str]]
        """
        Label IDs to remove from the thread. Between 1 and 10 IDs.
        A label ID that does not exist in the inbox returns a 404.
        """

    class RemoveResponse(BaseResponse):
        """
        RemoveResponse is the response of removing a thread.

        Attributes:
            object (str): The object type, always "inbox_thread"
            id (str): The ID of the thread
            deleted (bool): True when this call moved the thread to trash
        """

        object: str
        """
        The object type, always "inbox_thread".
        """
        id: str
        """
        The ID of the thread.
        """
        deleted: bool
        """
        True when this call moved the thread to ``trash``.
        False when the thread was already there.
        """

    @classmethod
    def list(cls, inbox_id: str, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve the threads in an inbox, most recently active first. The ``after``
        and ``before`` cursors take a thread ID, and only one of them can be passed.
        To find threads by text, sender, recipient, attachment, or date, use ``search``.
        see more: https://resend.com/docs/api-reference/inboxes/list-threads

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            params (Optional[ListParams]): Optional filter and pagination parameters

        Returns:
            ListResponse: A page of the threads of the inbox
        """
        path = build_inbox_query_path(
            f"/inboxes/{inbox_id}/threads",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = request.Request[InboxThreads.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def search(
        cls, inbox_id: str, params: Optional[SearchParams] = None
    ) -> SearchResponse:
        """
        Find threads by the text of their emails, who sent or received them,
        whether they have attachments, and their dates. Results are ordered by
        latest activity, newest first, and paginate like ``list``. Search can be
        up to about a minute behind new emails. With a ``query``, ``folders=sent``
        also requires the matching email to be one the inbox sent. When more than
        10,000 threads match, search covers the 10,000 with the newest matching email.
        see more: https://resend.com/docs/api-reference/inboxes/search-threads

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            params (Optional[SearchParams]): Optional search, filter and pagination parameters

        Returns:
            SearchResponse: A page of the matching threads
        """
        path = build_inbox_query_path(
            f"/inboxes/{inbox_id}/threads/search",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = request.Request[InboxThreads.SearchResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, inbox_id: str, thread_id: str) -> InboxThreadSummary:
        """
        Retrieve the summary of a thread. The emails in the thread are listed
        with ``Inboxes.Threads.Emails.list``.
        see more: https://resend.com/docs/api-reference/inboxes/get-thread

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            thread_id (str): The Thread ID.

        Returns:
            InboxThreadSummary: The thread summary
        """
        path = f"/inboxes/{inbox_id}/threads/{thread_id}"
        resp = request.Request[InboxThreadSummary](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> InboxThreadSummary:
        """
        Mark a thread read or unread, move it to a folder, or add and remove labels.
        At least one of ``read``, ``folder``, ``label_id``, ``add_label_ids``, or
        ``remove_label_ids`` is required. A label ID cannot be both added and
        removed in the same request. Moving a thread out of ``trash`` restores it
        and clears its deletion deadline.
        see more: https://resend.com/docs/api-reference/inboxes/update-thread

        Args:
            params (UpdateParams): The inbox ID, the thread ID and the changes

        Returns:
            InboxThreadSummary: The updated thread summary
        """
        path = f"/inboxes/{params['inbox_id']}/threads/{params['id']}"
        resp = request.Request[InboxThreadSummary](
            path=path, params=without_keys(params, "inbox_id", "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, inbox_id: str, thread_id: str) -> RemoveResponse:
        """
        Move a thread to ``trash`` and schedule it for deletion in 30 days. This is
        reversible. To restore the thread, update its ``folder`` to ``inbox``,
        ``archive``, or ``spam``, which also clears the deletion deadline.
        see more: https://resend.com/docs/api-reference/inboxes/delete-thread

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            thread_id (str): The Thread ID.

        Returns:
            RemoveResponse: The thread ID and whether this call moved it to trash
        """
        path = f"/inboxes/{inbox_id}/threads/{thread_id}"
        resp = request.Request[InboxThreads.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(
        cls, inbox_id: str, params: Optional[ListParams] = None
    ) -> ListResponse:
        """
        Retrieve the threads in an inbox, most recently active first (async).
        The ``after`` and ``before`` cursors take a thread ID, and only one of them
        can be passed. To find threads by text, sender, recipient, attachment, or
        date, use ``search_async``.
        see more: https://resend.com/docs/api-reference/inboxes/list-threads

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            params (Optional[ListParams]): Optional filter and pagination parameters

        Returns:
            ListResponse: A page of the threads of the inbox
        """
        path = build_inbox_query_path(
            f"/inboxes/{inbox_id}/threads",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = await AsyncRequest[InboxThreads.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def search_async(
        cls, inbox_id: str, params: Optional[SearchParams] = None
    ) -> SearchResponse:
        """
        Find threads by the text of their emails, who sent or received them,
        whether they have attachments, and their dates (async). Results are
        ordered by latest activity, newest first, and paginate like ``list``.
        Search can be up to about a minute behind new emails. With a ``query``,
        ``folders=sent`` also requires the matching email to be one the inbox
        sent. When more than 10,000 threads match, search covers the 10,000 with
        the newest matching email.
        see more: https://resend.com/docs/api-reference/inboxes/search-threads

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            params (Optional[SearchParams]): Optional search, filter and pagination parameters

        Returns:
            SearchResponse: A page of the matching threads
        """
        path = build_inbox_query_path(
            f"/inboxes/{inbox_id}/threads/search",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = await AsyncRequest[InboxThreads.SearchResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, inbox_id: str, thread_id: str) -> InboxThreadSummary:
        """
        Retrieve the summary of a thread (async). The emails in the thread are
        listed with ``Inboxes.Threads.Emails.list_async``.
        see more: https://resend.com/docs/api-reference/inboxes/get-thread

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            thread_id (str): The Thread ID.

        Returns:
            InboxThreadSummary: The thread summary
        """
        path = f"/inboxes/{inbox_id}/threads/{thread_id}"
        resp = await AsyncRequest[InboxThreadSummary](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> InboxThreadSummary:
        """
        Mark a thread read or unread, move it to a folder, or add and remove
        labels (async). At least one of ``read``, ``folder``, ``label_id``,
        ``add_label_ids``, or ``remove_label_ids`` is required. A label ID cannot
        be both added and removed in the same request. Moving a thread out of
        ``trash`` restores it and clears its deletion deadline.
        see more: https://resend.com/docs/api-reference/inboxes/update-thread

        Args:
            params (UpdateParams): The inbox ID, the thread ID and the changes

        Returns:
            InboxThreadSummary: The updated thread summary
        """
        path = f"/inboxes/{params['inbox_id']}/threads/{params['id']}"
        resp = await AsyncRequest[InboxThreadSummary](
            path=path, params=without_keys(params, "inbox_id", "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, inbox_id: str, thread_id: str) -> RemoveResponse:
        """
        Move a thread to ``trash`` and schedule it for deletion in 30 days (async).
        This is reversible. To restore the thread, update its ``folder`` to
        ``inbox``, ``archive``, or ``spam``, which also clears the deletion deadline.
        see more: https://resend.com/docs/api-reference/inboxes/delete-thread

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            thread_id (str): The Thread ID.

        Returns:
            RemoveResponse: The thread ID and whether this call moved it to trash
        """
        path = f"/inboxes/{inbox_id}/threads/{thread_id}"
        resp = await AsyncRequest[InboxThreads.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
