from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper

from ._topic import Topic


class Topics:

    class CreateTopicResponse(BaseResponse):
        """
        CreateTopicResponse is the type that wraps the response of the topic that was created

        Attributes:
            id (str): The ID of the created topic
        """

        id: str
        """
        The ID of the created topic
        """

    class CreateParams(TypedDict):
        name: str
        """
        The topic name. Max length is 50 characters.
        """
        default_subscription: str
        """
        The default subscription preference for new contacts. Possible values: opt_in or opt_out.
        This value cannot be changed later.
        """
        description: NotRequired[str]
        """
        The topic description. Max length is 200 characters.
        """

    class UpdateTopicResponse(BaseResponse):
        """
        UpdateTopicResponse is the type that wraps the response of the topic that was updated

        Attributes:
            id (str): The ID of the updated topic
        """

        id: str
        """
        The ID of the updated topic
        """

    class UpdateParams(TypedDict, total=False):
        name: str
        """
        The topic name. Max length is 50 characters.
        """
        description: str
        """
        The topic description. Max length is 200 characters.
        """

    class RemoveTopicResponse(BaseResponse):
        """
        RemoveTopicResponse is the type that wraps the response of the topic that was removed

        Attributes:
            object (str): The object type, "topic"
            id (str): The ID of the removed topic
            deleted (bool): Whether the topic was deleted
        """

        object: str
        """
        The object type, "topic"
        """
        id: str
        """
        The ID of the removed topic
        """
        deleted: bool
        """
        Whether the topic was deleted
        """

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of topics to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more topics (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more topics (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse type that wraps a list of topic objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[Topic]): A list of topic objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[Topic]
        """
        A list of topic objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateTopicResponse:
        """
        Create a topic.
        see more: https://resend.com/docs/api-reference/topics/create-topic

        Args:
            params (CreateParams): The topic creation parameters
                - name: The topic name (max 50 characters)
                - default_subscription: The default subscription preference ("opt_in" or "opt_out")
                - description: Optional topic description (max 200 characters)

        Returns:
            CreateTopicResponse: The created topic response with the topic ID
        """

        path = "/topics"
        resp = request.Request[Topics.CreateTopicResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str) -> Topic:
        """
        Retrieve a single topic by its ID.
        see more: https://resend.com/docs/api-reference/topics/get-topic

        Args:
            id (str): The topic ID

        Returns:
            Topic: The topic object
        """
        path = f"/topics/{id}"
        resp = request.Request[Topic](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, id: str, params: UpdateParams) -> UpdateTopicResponse:
        """
        Update an existing topic.
        see more: https://resend.com/docs/api-reference/topics/update-topic

        Args:
            id (str): The topic ID
            params (UpdateParams): The topic update parameters
                - name: Optional topic name (max 50 characters)
                - description: Optional topic description (max 200 characters)

        Returns:
            UpdateTopicResponse: The updated topic response with the topic ID
        """
        path = f"/topics/{id}"
        resp = request.Request[Topics.UpdateTopicResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, id: str) -> RemoveTopicResponse:
        """
        Delete a single topic.
        see more: https://resend.com/docs/api-reference/topics/delete-topic

        Args:
            id (str): The topic ID

        Returns:
            RemoveTopicResponse: The removed topic response
        """
        path = f"/topics/{id}"
        resp = request.Request[Topics.RemoveTopicResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of topics.
        see more: https://resend.com/docs/api-reference/topics/list-topics

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of topics to retrieve (max 100, min 1).
                  If not provided, all topics will be returned without pagination.
                - after: ID after which to retrieve more topics
                - before: ID before which to retrieve more topics

        Returns:
            ListResponse: A list of topic objects
        """
        base_path = "/topics"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Topics.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp
