from typing import List

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.inboxes._query import inbox_path, without_keys

from ._inbox_label import InboxLabel

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class InboxLabels:
    """
    InboxLabels manages the labels of an inbox. A label is a named, colored tag
    that belongs to one inbox.
    """

    class ListResponse(BaseResponse):
        """
        ListResponse is the list of labels on an inbox. The list is not paginated.

        Attributes:
            object (str): The object type, always "list"
            data (List[InboxLabel]): The labels on the inbox, oldest first
        """

        object: str
        """
        The object type, always "list".
        """
        data: List[InboxLabel]
        """
        The labels on the inbox, oldest first.
        """

    class CreateParams(TypedDict):
        """
        CreateParams are the parameters for creating a label on an inbox.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            name (str): The name of the label.
            color (NotRequired[str]): The color of the label, as a #RRGGBB hex color.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        name: str
        """
        The name of the label. Max 64 characters. Leading and trailing whitespace
        is trimmed. Must not match another label on the inbox, compared without case.
        """
        color: NotRequired[str]
        """
        The color of the label, as a ``#RRGGBB`` hex color. It is stored in uppercase.
        When omitted, a random color from the dashboard palette is used.
        """

    class CreateResponse(BaseResponse):
        """
        CreateResponse is the response of creating a label.

        Attributes:
            object (str): The object type, always "inbox_label"
            id (str): The ID of the label
        """

        object: str
        """
        The object type, always "inbox_label".
        """
        id: str
        """
        The ID of the label.
        """

    class UpdateParams(TypedDict):
        """
        UpdateParams are the parameters for updating a label.
        Omitted fields keep their current value.

        Attributes:
            inbox_id (str): The Inbox ID or the inbox email address.
            id (str): The Label ID.
            name (NotRequired[str]): A new name for the label.
            color (NotRequired[str]): A new color for the label, as a #RRGGBB hex color.
        """

        inbox_id: str
        """
        The Inbox ID or the inbox email address.
        """
        id: str
        """
        The Label ID.
        """
        name: NotRequired[str]
        """
        A new name for the label. Max 64 characters. Leading and trailing whitespace
        is trimmed. Must not match another label on the inbox, compared without case.
        """
        color: NotRequired[str]
        """
        A new color for the label, as a ``#RRGGBB`` hex color. It is stored in uppercase.
        """

    class UpdateResponse(BaseResponse):
        """
        UpdateResponse is the response of updating a label.

        Attributes:
            object (str): The object type, always "inbox_label"
            id (str): The ID of the updated label
        """

        object: str
        """
        The object type, always "inbox_label".
        """
        id: str
        """
        The ID of the updated label.
        """

    class RemoveResponse(BaseResponse):
        """
        RemoveResponse is the response of removing a label.

        Attributes:
            object (str): The object type, always "inbox_label"
            id (str): The ID of the removed label
            deleted (bool): Whether the label was deleted
        """

        object: str
        """
        The object type, always "inbox_label".
        """
        id: str
        """
        The ID of the removed label.
        """
        deleted: bool
        """
        Indicates whether the label was deleted.
        """

    @classmethod
    def list(cls, inbox_id: str) -> ListResponse:
        """
        Retrieve every label on an inbox, oldest first. The list is not paginated.
        see more: https://resend.com/docs/api-reference/inboxes/list-labels

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.

        Returns:
            ListResponse: The labels on the inbox
        """
        path = f"{inbox_path(inbox_id)}/labels"
        resp = request.Request[InboxLabels.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def create(cls, params: CreateParams) -> CreateResponse:
        """
        Create a label on an inbox. An inbox can have at most 100 labels. Label
        names are unique per inbox, compared without case. A duplicate name or a
        full inbox returns a 422 validation_error.
        see more: https://resend.com/docs/api-reference/inboxes/create-label

        Args:
            params (CreateParams): The inbox ID, the label name and an optional color

        Returns:
            CreateResponse: The object type and the ID of the label
        """
        path = f"{inbox_path(params['inbox_id'])}/labels"
        resp = request.Request[InboxLabels.CreateResponse](
            path=path, params=without_keys(params, "inbox_id"), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Rename or recolor a label. Omitted fields keep their current value. A new
        name must not match another label on the inbox, compared without case, or
        the request returns a 422 validation_error.
        see more: https://resend.com/docs/api-reference/inboxes/update-label

        Args:
            params (UpdateParams): The inbox ID, the label ID and the fields to change

        Returns:
            UpdateResponse: The object type and the ID of the updated label
        """
        path = f"{inbox_path(params['inbox_id'])}/labels/{params['id']}"
        resp = request.Request[InboxLabels.UpdateResponse](
            path=path, params=without_keys(params, "inbox_id", "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, inbox_id: str, label_id: str) -> RemoveResponse:
        """
        Delete a label and remove it from every thread that carries it.
        see more: https://resend.com/docs/api-reference/inboxes/delete-label

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            label_id (str): The Label ID.

        Returns:
            RemoveResponse: The removed label ID and its deleted status
        """
        path = f"{inbox_path(inbox_id)}/labels/{label_id}"
        resp = request.Request[InboxLabels.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, inbox_id: str) -> ListResponse:
        """
        Retrieve every label on an inbox, oldest first (async).
        The list is not paginated.
        see more: https://resend.com/docs/api-reference/inboxes/list-labels

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.

        Returns:
            ListResponse: The labels on the inbox
        """
        path = f"{inbox_path(inbox_id)}/labels"
        resp = await AsyncRequest[InboxLabels.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(cls, params: CreateParams) -> CreateResponse:
        """
        Create a label on an inbox (async). An inbox can have at most 100 labels.
        Label names are unique per inbox, compared without case. A duplicate name
        or a full inbox returns a 422 validation_error.
        see more: https://resend.com/docs/api-reference/inboxes/create-label

        Args:
            params (CreateParams): The inbox ID, the label name and an optional color

        Returns:
            CreateResponse: The object type and the ID of the label
        """
        path = f"{inbox_path(params['inbox_id'])}/labels"
        resp = await AsyncRequest[InboxLabels.CreateResponse](
            path=path, params=without_keys(params, "inbox_id"), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> UpdateResponse:
        """
        Rename or recolor a label (async). Omitted fields keep their current value.
        A new name must not match another label on the inbox, compared without
        case, or the request returns a 422 validation_error.
        see more: https://resend.com/docs/api-reference/inboxes/update-label

        Args:
            params (UpdateParams): The inbox ID, the label ID and the fields to change

        Returns:
            UpdateResponse: The object type and the ID of the updated label
        """
        path = f"{inbox_path(params['inbox_id'])}/labels/{params['id']}"
        resp = await AsyncRequest[InboxLabels.UpdateResponse](
            path=path, params=without_keys(params, "inbox_id", "id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, inbox_id: str, label_id: str) -> RemoveResponse:
        """
        Delete a label and remove it from every thread that carries it (async).
        see more: https://resend.com/docs/api-reference/inboxes/delete-label

        Args:
            inbox_id (str): The Inbox ID or the inbox email address.
            label_id (str): The Label ID.

        Returns:
            RemoveResponse: The removed label ID and its deleted status
        """
        path = f"{inbox_path(inbox_id)}/labels/{label_id}"
        resp = await AsyncRequest[InboxLabels.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
