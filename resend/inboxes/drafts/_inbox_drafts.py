from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.inboxes._query import (build_inbox_query_path, inbox_path,
                                   without_keys)

from ._inbox_draft import InboxDraft, InboxDraftListItem

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class InboxDrafts:
    """
    InboxDrafts manages the drafts of an inbox.
    """

    class AttachmentParams(TypedDict):
        """
        AttachmentParams is a file to store on a draft. Each one needs
        ``content``, ``filename`` and ``content_type``. A ``path`` or
        ``content_id`` returns a 422.

        Attributes:
            content (str): The content of the file, encoded in base64.
            filename (str): The name of the file.
            content_type (str): The MIME type of the file.
        """

        content: str
        """
        The content of the file, encoded in base64. It cannot be empty.
        """
        filename: str
        """
        The name of the file.
        """
        content_type: str
        """
        The MIME type of the file, for example ``application/pdf``.
        """

    class ListParams(TypedDict):
        """
        ListParams are the pagination parameters for listing drafts.
        The ``after`` and ``before`` cursors take a Draft ID from the current page.

        Attributes:
            limit (NotRequired[int]): Number of drafts to retrieve. Maximum is 100, minimum is 1.
            after (NotRequired[str]): The Draft ID after which to retrieve more drafts.
            before (NotRequired[str]): The Draft ID before which to retrieve more drafts.
        """

        limit: NotRequired[int]
        """
        Number of drafts to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The Draft ID after which we'll retrieve more drafts (for pagination).
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The Draft ID before which we'll retrieve more drafts (for pagination).
        Cannot be used with the after parameter.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is a page of the unsent drafts on an inbox.

        Attributes:
            object (str): The object type, always "list"
            has_more (bool): Whether there are more results available
            data (List[InboxDraftListItem]): The unsent drafts, most recently updated first
        """

        object: str
        """
        The object type, always "list".
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """
        data: List[InboxDraftListItem]
        """
        The unsent drafts on this page, most recently updated first.
        """

    class CreateParams(TypedDict):
        """
        CreateParams are the parameters for creating a draft. At least one of
        ``to``, ``cc``, ``bcc``, ``subject``, ``text``, ``html`` or ``attachments``
        must be non-empty.
        The combined recipients of ``to``, ``cc`` and ``bcc`` cannot exceed 50.
        ``thread_id`` and ``reply_to_email_id`` must be sent together or not at all.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            to (NotRequired[Optional[Union[str, List[str]]]]): The recipients.
            cc (NotRequired[Optional[Union[str, List[str]]]]): The CC recipients.
            bcc (NotRequired[Optional[Union[str, List[str]]]]): The BCC recipients.
            subject (NotRequired[Optional[str]]): The subject.
            html (NotRequired[Optional[str]]): The HTML body.
            text (NotRequired[Optional[str]]): The plain text body.
            attachments (NotRequired[List[AttachmentParams]]): Files to store on the draft.
            thread_id (NotRequired[str]): The Thread ID to reply in.
            reply_to_email_id (NotRequired[str]): The Email ID to reply to.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        to: NotRequired[Optional[Union[str, List[str]]]]
        """
        The recipients. For multiple addresses, send a list of strings. Each value
        can include a friendly name, for example ``Ada Lovelace <ada@example.org>``.
        """
        cc: NotRequired[Optional[Union[str, List[str]]]]
        """
        The CC recipients. For multiple addresses, send a list of strings.
        """
        bcc: NotRequired[Optional[Union[str, List[str]]]]
        """
        The BCC recipients. For multiple addresses, send a list of strings.
        """
        subject: NotRequired[Optional[str]]
        """
        The subject. Max 2000 characters. A string that is only whitespace, or
        that contains a line break, is rejected.
        """
        html: NotRequired[Optional[str]]
        """
        The HTML body.
        """
        text: NotRequired[Optional[str]]
        """
        The plain text body.
        """
        attachments: NotRequired[List["InboxDrafts.AttachmentParams"]]
        """
        Files to store on the draft. Each one needs ``content``, ``filename`` and
        ``content_type``. A ``path`` or ``content_id`` returns a 422. The files on
        a draft can total at most 25 MB. An empty file or a blocked file type
        returns a 422.
        """
        thread_id: NotRequired[str]
        """
        The Thread ID to reply in. Must be sent with ``reply_to_email_id``.
        """
        reply_to_email_id: NotRequired[str]
        """
        The Email ID to reply to, as returned in ``data[].id`` by the list thread
        emails endpoint. Must be sent with ``thread_id``.
        """

    class CreateOptions(TypedDict):
        """
        CreateOptions is the class that wraps the options for the create method.

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
        Between 1 and 256 characters, so the draft is created only once. A retry with the
        same key within 24 hours replays the first successful (2xx) response,
        with the ``idempotent-replayed: true`` header. A failed request is not
        stored, so you can retry it with the same key. Reusing the key with a
        different body, or while the first request is still running, returns a 409.
        """

    class CreateResponse(BaseResponse):
        """
        CreateResponse is the response of creating a draft.

        Attributes:
            object (str): The object type, always "inbox_draft"
            id (str): The ID of the draft
        """

        object: str
        """
        The object type, always "inbox_draft".
        """
        id: str
        """
        The ID of the draft.
        """

    class UpdateParams(TypedDict):
        """
        UpdateParams are the parameters for updating a draft. Send at least one of
        ``to``, ``cc``, ``bcc``, ``subject``, ``text``, ``html`` or ``attachments``.
        Omitted fields are left unchanged. Setting ``text`` or ``html`` replaces the whole body, so
        the body part you omit becomes None. The merged draft must contain at least
        one non-empty field, and its combined recipients cannot exceed 50.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            id (str): The Draft ID.
            to (NotRequired[Optional[Union[str, List[str]]]]): The recipients.
            cc (NotRequired[Optional[Union[str, List[str]]]]): The CC recipients.
            bcc (NotRequired[Optional[Union[str, List[str]]]]): The BCC recipients.
            subject (NotRequired[Optional[str]]): The subject.
            html (NotRequired[Optional[str]]): The HTML body.
            text (NotRequired[Optional[str]]): The plain text body.
            attachments (NotRequired[Optional[List[AttachmentParams]]]): Files that replace
                every attachment on the draft.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        id: str
        """
        The Draft ID.
        """
        to: NotRequired[Optional[Union[str, List[str]]]]
        """
        The recipients. For multiple addresses, send a list of strings. Each value
        can include a friendly name. Pass None to clear.
        """
        cc: NotRequired[Optional[Union[str, List[str]]]]
        """
        The CC recipients. Pass None or ``[]`` to clear.
        """
        bcc: NotRequired[Optional[Union[str, List[str]]]]
        """
        The BCC recipients. Pass None or ``[]`` to clear.
        """
        subject: NotRequired[Optional[str]]
        """
        The subject. Max 2000 characters. Must not contain a line break.
        Pass None to clear.
        """
        html: NotRequired[Optional[str]]
        """
        The HTML body. Pass None to clear.
        """
        text: NotRequired[Optional[str]]
        """
        The plain text body. Pass None to clear.
        """
        attachments: NotRequired[Optional[List["InboxDrafts.AttachmentParams"]]]
        """
        Files to store on the draft. Each one needs ``content``, ``filename`` and
        ``content_type``. A ``path`` or ``content_id`` returns a 422. The files on
        a draft can total at most 25 MB. An empty file or a blocked file type
        returns a 422. Sending the field replaces every attachment on the draft.
        Send ``[]`` or None to remove them all.
        """

    class UpdateResponse(BaseResponse):
        """
        UpdateResponse is the response of updating a draft.

        Attributes:
            object (str): The object type, always "inbox_draft"
            id (str): The ID of the draft
        """

        object: str
        """
        The object type, always "inbox_draft".
        """
        id: str
        """
        The ID of the draft.
        """

    class RemoveResponse(BaseResponse):
        """
        RemoveResponse is the response of removing a draft.

        Attributes:
            object (str): The object type, always "inbox_draft"
            id (str): The ID of the draft
            deleted (bool): Whether the draft was deleted
        """

        object: str
        """
        The object type, always "inbox_draft".
        """
        id: str
        """
        The ID of the draft.
        """
        deleted: bool
        """
        Indicates whether the draft was successfully deleted.
        """

    class SendParams(TypedDict):
        """
        SendParams are the optional body parameters for sending a draft.

        Attributes:
            headers (NotRequired[Dict[str, str]]): Custom headers to be added to the email.
        """

        headers: NotRequired[Dict[str, str]]
        """
        Custom headers to be added to the email. The ``In-Reply-To``,
        ``References`` and ``Reply-To`` headers are set by Resend and cannot be
        set here. Sending one of them, in any letter case, returns a 422. Header
        names cannot be empty, and names and values cannot contain line breaks
        or null characters, or the request returns a 422.
        """

    class SendOptions(TypedDict):
        """
        SendOptions is the class that wraps the options for the send method.

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
        Between 1 and 256 characters, so the draft is sent only once. A retry with the
        same key within 24 hours replays the first successful (2xx) response,
        with the ``idempotent-replayed: true`` header. A failed request is not
        stored, so you can retry it with the same key. Reusing the key with a
        different body, or while the first request is still running, returns a 409.
        """

    class SendResponse(BaseResponse):
        """
        SendResponse is the response of sending a draft.

        Attributes:
            id (str): The ID of the sent email
        """

        id: str
        """
        The ID of the sent email. Use it with the emails endpoints.
        """

    @classmethod
    def list(cls, inbox_id: str, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve the unsent drafts on an inbox, most recently updated first.
        A cursor that is not an unsent draft on this inbox returns a 404.
        see more: https://resend.com/docs/api-reference/inboxes/list-drafts

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            params (Optional[ListParams]): Optional pagination parameters

        Returns:
            ListResponse: A page of the unsent drafts
        """
        path = build_inbox_query_path(
            f"{inbox_path(inbox_id)}/drafts",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = request.Request[InboxDrafts.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def create(
        cls, params: CreateParams, options: Optional[CreateOptions] = None
    ) -> CreateResponse:
        """
        Create an unsent draft on an inbox. Omit ``thread_id`` and
        ``reply_to_email_id`` for a draft that starts a new thread. Pass both
        together for a reply draft in an existing thread. A reply draft without
        ``to`` is addressed to the sender of the email it replies to, or to its
        Reply-To when set. For an email the inbox sent, it defaults to that email's
        ``to`` recipients. Send ``to: []`` to leave it empty. Attachments are
        stored on the draft, so each one needs ``content``, ``filename`` and
        ``content_type``. Only one unsent reply draft can target an email, so a
        reply draft request for an email that already has one returns the ID of
        the existing draft. That request ignores every other field, except
        ``attachments``, which replaces the attachments of the existing draft. A
        reply draft created without ``subject`` stores an empty subject and gets
        no ``Re:`` prefix, so set one before you send it.
        see more: https://resend.com/docs/api-reference/inboxes/create-draft

        Args:
            params (CreateParams): The inbox ID and the content of the draft
            options (Optional[CreateOptions]): The create options, ie: idempotency_key

        Returns:
            CreateResponse: The object type and the ID of the draft
        """
        path = f"{inbox_path(params['inbox_id'])}/drafts"
        resp = request.Request[InboxDrafts.CreateResponse](
            path=path,
            params=without_keys(params, "inbox_id"),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, inbox_id: str, draft_id: str) -> InboxDraft:
        """
        Retrieve a single draft.
        see more: https://resend.com/docs/api-reference/inboxes/get-draft

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            draft_id (str): The Draft ID.

        Returns:
            InboxDraft: The draft
        """
        path = f"{inbox_path(inbox_id)}/drafts/{draft_id}"
        resp = request.Request[InboxDraft](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update the content of an unsent draft. Omitted fields are left unchanged.
        Sending ``attachments`` replaces every attachment on the draft. A request
        that sets ``text`` or ``html`` replaces the whole body. The body part you
        omit from that request becomes None. A draft that was already sent, or
        that changed during the request, returns a 409.
        see more: https://resend.com/docs/api-reference/inboxes/update-draft

        Args:
            params (UpdateParams): The inbox ID, the draft ID and the fields to change

        Returns:
            UpdateResponse: The object type and the ID of the draft
        """
        path = f"{inbox_path(params['inbox_id'])}/drafts/{params['id']}"
        resp = request.Request[InboxDrafts.UpdateResponse](
            path=path, params=without_keys(params, "inbox_id", "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, inbox_id: str, draft_id: str) -> RemoveResponse:
        """
        Discard an unsent draft. A draft that was already sent, or that changed
        during the request, returns a 409.
        see more: https://resend.com/docs/api-reference/inboxes/delete-draft

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            draft_id (str): The Draft ID.

        Returns:
            RemoveResponse: The draft ID and its deleted status
        """
        path = f"{inbox_path(inbox_id)}/drafts/{draft_id}"
        resp = request.Request[InboxDrafts.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    def send(
        cls,
        inbox_id: str,
        draft_id: str,
        params: Optional[SendParams] = None,
        options: Optional[SendOptions] = None,
    ) -> SendResponse:
        """
        Send a draft from the inbox address. A reply draft is sent in its thread.
        A draft without a thread starts a new thread. The draft must have at least
        one ``to`` recipient, a non-empty ``subject``, and ``html`` or ``text``,
        or the request returns a 422. A draft that was already sent returns a 409.
        The request body is optional and takes only ``headers``.
        see more: https://resend.com/docs/api-reference/inboxes/send-draft

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            draft_id (str): The Draft ID.
            params (Optional[SendParams]): Optional body parameters, ie: headers
            options (Optional[SendOptions]): The send options, ie: idempotency_key

        Returns:
            SendResponse: The ID of the sent email
        """
        path = f"{inbox_path(inbox_id)}/drafts/{draft_id}/send"
        resp = request.Request[InboxDrafts.SendResponse](
            path=path,
            params=cast(Dict[Any, Any], params) if params else {},
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(
        cls, inbox_id: str, params: Optional[ListParams] = None
    ) -> ListResponse:
        """
        Retrieve the unsent drafts on an inbox, most recently updated first (async).
        A cursor that is not an unsent draft on this inbox returns a 404.
        see more: https://resend.com/docs/api-reference/inboxes/list-drafts

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            params (Optional[ListParams]): Optional pagination parameters

        Returns:
            ListResponse: A page of the unsent drafts
        """
        path = build_inbox_query_path(
            f"{inbox_path(inbox_id)}/drafts",
            cast(Dict[Any, Any], params) if params else None,
        )
        resp = await AsyncRequest[InboxDrafts.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(
        cls, params: CreateParams, options: Optional[CreateOptions] = None
    ) -> CreateResponse:
        """
        Create an unsent draft on an inbox (async). Omit ``thread_id`` and
        ``reply_to_email_id`` for a draft that starts a new thread. Pass both
        together for a reply draft in an existing thread. A reply draft without
        ``to`` is addressed to the sender of the email it replies to, or to its
        Reply-To when set. For an email the inbox sent, it defaults to that email's
        ``to`` recipients. Send ``to: []`` to leave it empty. Attachments are
        stored on the draft, so each one needs ``content``, ``filename`` and
        ``content_type``. Only one unsent reply draft can target an email, so a
        reply draft request for an email that already has one returns the ID of
        the existing draft. That request ignores every other field, except
        ``attachments``, which replaces the attachments of the existing draft. A
        reply draft created without ``subject`` stores an empty subject and gets
        no ``Re:`` prefix, so set one before you send it.
        see more: https://resend.com/docs/api-reference/inboxes/create-draft

        Args:
            params (CreateParams): The inbox ID and the content of the draft
            options (Optional[CreateOptions]): The create options, ie: idempotency_key

        Returns:
            CreateResponse: The object type and the ID of the draft
        """
        path = f"{inbox_path(params['inbox_id'])}/drafts"
        resp = await AsyncRequest[InboxDrafts.CreateResponse](
            path=path,
            params=without_keys(params, "inbox_id"),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, inbox_id: str, draft_id: str) -> InboxDraft:
        """
        Retrieve a single draft (async).
        see more: https://resend.com/docs/api-reference/inboxes/get-draft

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            draft_id (str): The Draft ID.

        Returns:
            InboxDraft: The draft
        """
        path = f"{inbox_path(inbox_id)}/drafts/{draft_id}"
        resp = await AsyncRequest[InboxDraft](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update the content of an unsent draft (async). Omitted fields are left
        unchanged. Sending ``attachments`` replaces every attachment on the draft.
        A request that sets ``text`` or ``html`` replaces the whole body.
        The body part you omit from that request becomes None. A draft that was
        already sent, or that changed during the request, returns a 409.
        see more: https://resend.com/docs/api-reference/inboxes/update-draft

        Args:
            params (UpdateParams): The inbox ID, the draft ID and the fields to change

        Returns:
            UpdateResponse: The object type and the ID of the draft
        """
        path = f"{inbox_path(params['inbox_id'])}/drafts/{params['id']}"
        resp = await AsyncRequest[InboxDrafts.UpdateResponse](
            path=path, params=without_keys(params, "inbox_id", "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, inbox_id: str, draft_id: str) -> RemoveResponse:
        """
        Discard an unsent draft (async). A draft that was already sent, or that
        changed during the request, returns a 409.
        see more: https://resend.com/docs/api-reference/inboxes/delete-draft

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            draft_id (str): The Draft ID.

        Returns:
            RemoveResponse: The draft ID and its deleted status
        """
        path = f"{inbox_path(inbox_id)}/drafts/{draft_id}"
        resp = await AsyncRequest[InboxDrafts.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def send_async(
        cls,
        inbox_id: str,
        draft_id: str,
        params: Optional[SendParams] = None,
        options: Optional[SendOptions] = None,
    ) -> SendResponse:
        """
        Send a draft from the inbox address (async). A reply draft is sent in its
        thread. A draft without a thread starts a new thread. The draft must have
        at least one ``to`` recipient, a non-empty ``subject``, and ``html`` or
        ``text``, or the request returns a 422. A draft that was already sent
        returns a 409. The request body is optional and takes only ``headers``.
        see more: https://resend.com/docs/api-reference/inboxes/send-draft

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            draft_id (str): The Draft ID.
            params (Optional[SendParams]): Optional body parameters, ie: headers
            options (Optional[SendOptions]): The send options, ie: idempotency_key

        Returns:
            SendResponse: The ID of the sent email
        """
        path = f"{inbox_path(inbox_id)}/drafts/{draft_id}/send"
        resp = await AsyncRequest[InboxDrafts.SendResponse](
            path=path,
            params=cast(Dict[Any, Any], params) if params else {},
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp
