from typing import List

from typing_extensions import TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.inboxes._query import inbox_path, without_keys
from resend.inboxes.threads._inbox_thread import InboxThreadLabel

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class InboxThreadLabels:
    """
    InboxThreadLabels manages the labels on an inbox thread. To create, rename
    or delete the labels themselves, use ``Inboxes.Labels``.
    """

    class ListResponse(BaseResponse):
        """
        ListResponse lists every label on the thread after the change.

        Attributes:
            object (str): The object type, always "list"
            data (List[InboxThreadLabel]): The labels on the thread
        """

        object: str
        """
        The object type, always "list".
        """
        data: List[InboxThreadLabel]
        """
        The labels on the thread after the change.
        """

    class AddParams(TypedDict):
        """
        AddParams are the parameters for adding labels to a thread.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            labels (List[str]): The IDs of the labels to apply to the thread.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        thread_id: str
        """
        The Thread ID.
        """
        labels: List[str]
        """
        The IDs of the labels to apply to the thread. Between 1 and 10 IDs,
        each a label of the inbox.
        """

    class SetParams(TypedDict):
        """
        SetParams are the parameters for replacing the labels of a thread.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            labels (List[str]): The IDs of the labels the thread carries after the change.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        thread_id: str
        """
        The Thread ID.
        """
        labels: List[str]
        """
        The IDs of the labels the thread carries after the change. Up to 100 IDs,
        each a label of the inbox. Pass an empty list to take every label off
        the thread.
        """

    @classmethod
    def add(cls, params: AddParams) -> ListResponse:
        """
        Apply one or more labels to a thread. Labels already on the thread stay
        on it. A label ID that is not a label of the inbox returns a 404, and
        nothing changes. To replace the labels of the thread, use ``set``.
        see more: https://resend.com/docs/api-reference/inboxes/add-thread-labels

        Args:
            params (AddParams): The inbox ID, the thread ID and the label IDs

        Returns:
            ListResponse: Every label on the thread after the change
        """
        path = f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}/labels"
        resp = request.Request[InboxThreadLabels.ListResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id"),
            verb="post",
        ).perform_with_content()
        return resp

    @classmethod
    def set(cls, params: SetParams) -> ListResponse:
        """
        Replace every label on a thread with the given labels, in one atomic
        change. The labels themselves are kept. An empty list takes every label
        off the thread. A label ID that is not a label of the inbox returns a
        404, and nothing changes.
        see more: https://resend.com/docs/api-reference/inboxes/set-thread-labels

        Args:
            params (SetParams): The inbox ID, the thread ID and the label IDs

        Returns:
            ListResponse: Every label on the thread after the change
        """
        path = f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}/labels"
        resp = request.Request[InboxThreadLabels.ListResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id"),
            verb="put",
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, inbox_id: str, thread_id: str, label_id: str) -> ListResponse:
        """
        Take one label off a thread. The label itself is kept, and stays on every
        other thread that carries it. A label that is not on the thread returns
        the current labels. To delete the label, use ``Inboxes.Labels.remove``.
        see more: https://resend.com/docs/api-reference/inboxes/remove-thread-label

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            label_id (str): The Label ID.

        Returns:
            ListResponse: Every label on the thread after the change
        """
        path = f"{inbox_path(inbox_id)}/threads/{thread_id}/labels/{label_id}"
        resp = request.Request[InboxThreadLabels.ListResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def add_async(cls, params: AddParams) -> ListResponse:
        """
        Apply one or more labels to a thread (async). Labels already on the
        thread stay on it. A label ID that is not a label of the inbox returns a
        404, and nothing changes. To replace the labels of the thread, use
        ``set_async``.
        see more: https://resend.com/docs/api-reference/inboxes/add-thread-labels

        Args:
            params (AddParams): The inbox ID, the thread ID and the label IDs

        Returns:
            ListResponse: Every label on the thread after the change
        """
        path = f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}/labels"
        resp = await AsyncRequest[InboxThreadLabels.ListResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id"),
            verb="post",
        ).perform_with_content()
        return resp

    @classmethod
    async def set_async(cls, params: SetParams) -> ListResponse:
        """
        Replace every label on a thread with the given labels, in one atomic
        change (async). The labels themselves are kept. An empty list takes every
        label off the thread. A label ID that is not a label of the inbox returns
        a 404, and nothing changes.
        see more: https://resend.com/docs/api-reference/inboxes/set-thread-labels

        Args:
            params (SetParams): The inbox ID, the thread ID and the label IDs

        Returns:
            ListResponse: Every label on the thread after the change
        """
        path = f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}/labels"
        resp = await AsyncRequest[InboxThreadLabels.ListResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id"),
            verb="put",
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(
        cls, inbox_id: str, thread_id: str, label_id: str
    ) -> ListResponse:
        """
        Take one label off a thread (async). The label itself is kept, and stays
        on every other thread that carries it. A label that is not on the thread
        returns the current labels. To delete the label, use
        ``Inboxes.Labels.remove_async``.
        see more: https://resend.com/docs/api-reference/inboxes/remove-thread-label

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            label_id (str): The Label ID.

        Returns:
            ListResponse: Every label on the thread after the change
        """
        path = f"{inbox_path(inbox_id)}/threads/{thread_id}/labels/{label_id}"
        resp = await AsyncRequest[InboxThreadLabels.ListResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
