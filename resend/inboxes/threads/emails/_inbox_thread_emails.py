from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.emails._attachment import Attachment, RemoteAttachment
from resend.inboxes._query import (build_inbox_query_path, inbox_path,
                                   without_keys)

from ._inbox_thread_email import InboxThreadEmail

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class InboxThreadEmails:
    """
    InboxThreadEmails manages the messages of an inbox thread.
    """

    class ListParams(TypedDict):
        """
        ListParams are the pagination parameters for listing the messages of a thread.
        Pass the ``id`` of the last message as ``after`` to get the next, newer page.
        Pass the ``id`` of the first message as ``before`` to get the previous, older page.

        Attributes:
            limit (NotRequired[int]): Number of messages to retrieve. Maximum is 100, minimum is 1.
            after (NotRequired[str]): The message ID after which to retrieve more messages.
            before (NotRequired[str]): The message ID before which to retrieve more messages.
        """

        limit: NotRequired[int]
        """
        Number of messages to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The message ID after which we'll retrieve more messages (for pagination).
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The message ID before which we'll retrieve more messages (for pagination).
        Cannot be used with the after parameter.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is a page of the messages of a thread.

        Attributes:
            object (str): The object type, always "list"
            has_more (bool): Whether there are more results available
            data (List[InboxThreadEmail]): The messages on this page, oldest first
        """

        object: str
        """
        The object type, always "list".
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """
        data: List[InboxThreadEmail]
        """
        The messages of the thread on this page, oldest first.
        """

    class ReplyParams(TypedDict):
        """
        ReplyParams are the parameters for replying to a thread email.
        At least one of ``html`` or ``text`` must contain more than whitespace.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            email_id (str): The Email ID of the message to reply to.
            html (NotRequired[str]): The HTML body of the reply.
            text (NotRequired[str]): The plain-text body of the reply.
            cc (NotRequired[Union[str, List[str]]]): CC recipients.
            bcc (NotRequired[Union[str, List[str]]]): BCC recipients.
            subject (NotRequired[str]): The subject of the reply.
            reply_all (NotRequired[bool]): Reply to everyone on the original message.
            headers (NotRequired[Dict[str, str]]): Custom headers to be added to the email.
            attachments (NotRequired[List[Union[Attachment, RemoteAttachment]]]): Files to attach.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        thread_id: str
        """
        The Thread ID.
        """
        email_id: str
        """
        The Email ID of the message to reply to, as returned in ``data[].id``
        by the list thread emails endpoint.
        """
        html: NotRequired[str]
        """
        The HTML body of the reply.
        """
        text: NotRequired[str]
        """
        The plain-text body of the reply.
        """
        cc: NotRequired[Union[str, List[str]]]
        """
        CC recipient email address. For multiple addresses, send a list of strings.
        Without ``reply_all``, the reply copies only these addresses. With
        ``reply_all``, these addresses are merged with the copied recipients,
        without duplicates. ``cc`` and ``bcc`` combined must be fewer than 50
        addresses. After the ``to`` recipients are added, the reply cannot exceed
        50 recipients.
        """
        bcc: NotRequired[Union[str, List[str]]]
        """
        BCC recipient email address. For multiple addresses, send a list of strings.
        BCC recipients of the original message are never copied.
        """
        subject: NotRequired[str]
        """
        The subject of the reply. Cannot contain a line break. When omitted, the
        thread subject is used, prefixed with ``Re:`` if it does not already start with it.
        """
        reply_all: NotRequired[bool]
        """
        Reply to everyone on the original message. For a message the inbox
        received, the reply goes to its ``Reply-To`` addresses, or to its sender
        when it has none, and copies the other addresses of its ``To`` header and
        its ``cc`` recipients in ``cc``. For a message the inbox sent, the reply
        goes to that message's ``Reply-To`` addresses when they are not the inbox
        address, otherwise to its ``to`` recipients, and copies its ``cc``
        recipients. The inbox address is always excluded, and duplicates are
        removed. Defaults to False.
        """
        headers: NotRequired[Dict[str, str]]
        """
        Custom headers to be added to the email. The ``In-Reply-To``,
        ``References`` and ``Reply-To`` headers are set by Resend and cannot be
        set here. Sending one of them, in any letter case, returns a 422. Header
        names cannot be empty, and names and values cannot contain line breaks
        or null characters, or the request returns a 422.
        """
        attachments: NotRequired[List[Union[Attachment, RemoteAttachment]]]
        """
        Files to attach, as on ``Emails.send``. Each one needs ``content`` or
        ``path``. The ``content`` of all files can total at most 25 MB. A
        ``path`` file does not count toward the 25 MB, because it is fetched when
        the email is sent.
        An empty file, a blocked file type, or a ``path`` that is not an ``http``
        or ``https`` URL or points to ``localhost`` returns a 422.
        """

    class ReplyOptions(TypedDict):
        """
        ReplyOptions is the class that wraps the options for the reply method.

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
        Between 1 and 256 characters, so the reply is sent only once. A retry with the
        same key within 24 hours replays the first successful (2xx) response,
        with the ``idempotent-replayed: true`` header. A failed request is not
        stored, so you can retry it with the same key. Reusing the key with a
        different body, or while the first request is still running, returns a 409.
        """

    class ReplyResponse(BaseResponse):
        """
        ReplyResponse is the response of replying to a thread email.

        Attributes:
            id (str): The ID of the sent email
        """

        id: str
        """
        The ID of the sent email. Use it with the emails endpoints.
        """

    class ForwardParams(TypedDict):
        """
        ForwardParams are the parameters for forwarding a thread email.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            email_id (str): The Email ID of the message to forward.
            to (Union[str, List[str]]): The recipients.
            cc (NotRequired[Union[str, List[str]]]): CC recipients.
            bcc (NotRequired[Union[str, List[str]]]): BCC recipients.
            html (NotRequired[str]): An HTML note sent above the quoted original.
            text (NotRequired[str]): A plain-text note sent above the quoted original.
            subject (NotRequired[str]): The subject of the forward.
            headers (NotRequired[Dict[str, str]]): Custom headers to be added to the email.
            attachments (NotRequired[List[Union[Attachment, RemoteAttachment]]]): Files to attach.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        thread_id: str
        """
        The Thread ID.
        """
        email_id: str
        """
        The Email ID of the message to forward, as returned in ``data[].id``
        by the list thread emails endpoint.
        """
        to: Union[str, List[str]]
        """
        Recipient email address. For multiple addresses, send a list of strings.
        Must name at least one address. ``to``, ``cc`` and ``bcc`` combined cannot
        exceed 50 recipients.
        """
        cc: NotRequired[Union[str, List[str]]]
        """
        CC recipient email address. For multiple addresses, send a list of strings.
        Counts toward the 50-recipient limit.
        """
        bcc: NotRequired[Union[str, List[str]]]
        """
        BCC recipient email address. For multiple addresses, send a list of strings.
        Counts toward the 50-recipient limit.
        """
        html: NotRequired[str]
        """
        An HTML note sent above the quoted original.
        """
        text: NotRequired[str]
        """
        A plain-text note sent above the quoted original.
        """
        subject: NotRequired[str]
        """
        The subject of the forward. Cannot contain a line break. When omitted, the
        thread subject is used, prefixed with ``Fwd:`` if it does not already start with it.
        """
        headers: NotRequired[Dict[str, str]]
        """
        Custom headers to be added to the email. The ``In-Reply-To``,
        ``References`` and ``Reply-To`` headers are set by Resend and cannot be
        set here. Sending one of them, in any letter case, returns a 422. Header
        names cannot be empty, and names and values cannot contain line breaks
        or null characters, or the request returns a 422.
        """
        attachments: NotRequired[List[Union[Attachment, RemoteAttachment]]]
        """
        Files to attach, as on ``Emails.send``. Each one needs ``content`` or
        ``path``. They share one limit with the attachments of the original
        message, which the forward also sends. Together they can have at most
        25 MB of ``content``. A ``path`` file does not count toward the 25 MB,
        because it is fetched when the email is sent.
        An empty file, a blocked file type, or a ``path`` that is not an ``http``
        or ``https`` URL or points to ``localhost`` returns a 422.
        """

    class ForwardOptions(TypedDict):
        """
        ForwardOptions is the class that wraps the options for the forward method.

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
        Between 1 and 256 characters, so the forward is sent only once. A retry with the
        same key within 24 hours replays the first successful (2xx) response,
        with the ``idempotent-replayed: true`` header. A failed request is not
        stored, so you can retry it with the same key. Reusing the key with a
        different body, or while the first request is still running, returns a 409.
        """

    class ForwardResponse(BaseResponse):
        """
        ForwardResponse is the response of forwarding a thread email.

        Attributes:
            id (str): The ID of the sent email
        """

        id: str
        """
        The ID of the sent email. Use it with the emails endpoints.
        """

    @classmethod
    def list(
        cls, inbox_id: str, thread_id: str, params: Optional[ListParams] = None
    ) -> ListResponse:
        """
        Retrieve the messages of a thread, oldest first. You cannot combine
        ``after`` and ``before``. A cursor that is not a message of the thread
        returns a 404.
        see more: https://resend.com/docs/api-reference/inboxes/list-thread-emails

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            params (Optional[ListParams]): Optional pagination parameters

        Returns:
            ListResponse: A page of the messages of the thread
        """
        path = build_inbox_query_path(
            f"{inbox_path(inbox_id)}/threads/{thread_id}/emails",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = request.Request[InboxThreadEmails.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, inbox_id: str, thread_id: str, email_id: str) -> InboxThreadEmail:
        """
        Retrieve a single thread email.
        see more: https://resend.com/docs/api-reference/inboxes/get-thread-email

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            email_id (str): The Email ID, as returned in ``data[].id`` by the list
                thread emails endpoint.

        Returns:
            InboxThreadEmail: The thread email
        """
        path = f"{inbox_path(inbox_id)}/threads/{thread_id}/emails/{email_id}"
        resp = request.Request[InboxThreadEmail](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def reply(
        cls, params: ReplyParams, options: Optional[ReplyOptions] = None
    ) -> ReplyResponse:
        """
        Send a reply from the inbox address right away, with no stored draft.
        The ``to`` recipients come from the message you reply to. For a message
        the inbox received, the reply goes to its ``Reply-To`` addresses, or to
        its sender when it has no ``Reply-To``. For a message the inbox sent, the
        reply goes to that message's ``to`` recipients. Set ``reply_all`` to also
        copy the other recipients of the message. The reply threads under the
        message through the ``In-Reply-To`` and ``References`` headers.
        see more: https://resend.com/docs/api-reference/inboxes/reply-thread-email

        Args:
            params (ReplyParams): The path IDs and the content of the reply
            options (Optional[ReplyOptions]): The reply options, ie: idempotency_key

        Returns:
            ReplyResponse: The ID of the sent email
        """
        path = (
            f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}"
            f"/emails/{params['email_id']}/reply"
        )
        resp = request.Request[InboxThreadEmails.ReplyResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id", "email_id"),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    def forward(
        cls, params: ForwardParams, options: Optional[ForwardOptions] = None
    ) -> ForwardResponse:
        """
        Forward a message from the inbox address right away, with no stored draft.
        The original message is quoted under a forwarded-message banner, below the
        optional ``html`` or ``text`` note. The attachments of the original message
        are sent with the forward, together with any ``attachments`` you add.
        The request fails when they exceed 25 MB of ``content`` in total.
        An original attachment that was sent from a URL (``path``) cannot be
        forwarded, and the request returns a 422.
        see more: https://resend.com/docs/api-reference/inboxes/forward-thread-email

        Args:
            params (ForwardParams): The path IDs, the recipients and the note
            options (Optional[ForwardOptions]): The forward options, ie: idempotency_key

        Returns:
            ForwardResponse: The ID of the sent email
        """
        path = (
            f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}"
            f"/emails/{params['email_id']}/forward"
        )
        resp = request.Request[InboxThreadEmails.ForwardResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id", "email_id"),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(
        cls, inbox_id: str, thread_id: str, params: Optional[ListParams] = None
    ) -> ListResponse:
        """
        Retrieve the messages of a thread, oldest first (async). You cannot
        combine ``after`` and ``before``. A cursor that is not a message of the
        thread returns a 404.
        see more: https://resend.com/docs/api-reference/inboxes/list-thread-emails

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            params (Optional[ListParams]): Optional pagination parameters

        Returns:
            ListResponse: A page of the messages of the thread
        """
        path = build_inbox_query_path(
            f"{inbox_path(inbox_id)}/threads/{thread_id}/emails",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = await AsyncRequest[InboxThreadEmails.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(
        cls, inbox_id: str, thread_id: str, email_id: str
    ) -> InboxThreadEmail:
        """
        Retrieve a single thread email (async).
        see more: https://resend.com/docs/api-reference/inboxes/get-thread-email

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            thread_id (str): The Thread ID.
            email_id (str): The Email ID, as returned in ``data[].id`` by the list
                thread emails endpoint.

        Returns:
            InboxThreadEmail: The thread email
        """
        path = f"{inbox_path(inbox_id)}/threads/{thread_id}/emails/{email_id}"
        resp = await AsyncRequest[InboxThreadEmail](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def reply_async(
        cls, params: ReplyParams, options: Optional[ReplyOptions] = None
    ) -> ReplyResponse:
        """
        Send a reply from the inbox address right away, with no stored draft (async).
        The ``to`` recipients come from the message you reply to. For a message
        the inbox received, the reply goes to its ``Reply-To`` addresses, or to
        its sender when it has no ``Reply-To``. For a message the inbox sent, the
        reply goes to that message's ``to`` recipients. Set ``reply_all`` to also
        copy the other recipients of the message. The reply threads under the
        message through the ``In-Reply-To`` and ``References`` headers.
        see more: https://resend.com/docs/api-reference/inboxes/reply-thread-email

        Args:
            params (ReplyParams): The path IDs and the content of the reply
            options (Optional[ReplyOptions]): The reply options, ie: idempotency_key

        Returns:
            ReplyResponse: The ID of the sent email
        """
        path = (
            f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}"
            f"/emails/{params['email_id']}/reply"
        )
        resp = await AsyncRequest[InboxThreadEmails.ReplyResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id", "email_id"),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    async def forward_async(
        cls, params: ForwardParams, options: Optional[ForwardOptions] = None
    ) -> ForwardResponse:
        """
        Forward a message from the inbox address right away, with no stored
        draft (async). The original message is quoted under a forwarded-message
        banner, below the optional ``html`` or ``text`` note. The attachments of
        the original message are sent with the forward, together with any
        ``attachments`` you add. The request fails when they exceed 25 MB of
        ``content`` in total. An original attachment that was sent from a URL
        (``path``) cannot be forwarded, and the request returns a 422.
        see more: https://resend.com/docs/api-reference/inboxes/forward-thread-email

        Args:
            params (ForwardParams): The path IDs, the recipients and the note
            options (Optional[ForwardOptions]): The forward options, ie: idempotency_key

        Returns:
            ForwardResponse: The ID of the sent email
        """
        path = (
            f"{inbox_path(params['inbox_id'])}/threads/{params['thread_id']}"
            f"/emails/{params['email_id']}/forward"
        )
        resp = await AsyncRequest[InboxThreadEmails.ForwardResponse](
            path=path,
            params=without_keys(params, "inbox_id", "thread_id", "email_id"),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp
