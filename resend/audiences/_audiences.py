from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.pagination_helper import PaginationHelper

from ._audience import Audience


class Audiences:

    class RemoveAudienceResponse(TypedDict):
        """
        RemoveAudienceResponse is the type that wraps the response of the audience that was removed

        Attributes:
            object (str): The object type, "audience"
            id (str): The ID of the removed audience
            deleted (bool): Whether the audience was deleted
        """

        object: str
        """
        The object type, "audience"
        """
        id: str
        """
        The ID of the removed audience
        """
        deleted: bool
        """
        Whether the audience was deleted
        """

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of audiences to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more audiences (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more audiences (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of audience objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[Audience]): A list of audience objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[Audience]
        """
        A list of audience objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class CreateAudienceResponse(TypedDict):
        """
        CreateAudienceResponse is the type that wraps the response of the audience that was created

        Attributes:
            object (str): The object type, "audience"
            id (str): The ID of the created audience
            name (str): The name of the created audience
        """

        object: str
        """
        The object type, "audience"
        """
        id: str
        """
        The ID of the created audience
        """
        name: str
        """
        The name of the created audience
        """

    class CreateParams(TypedDict):
        name: str
        """
        The name of the audience.
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateAudienceResponse:
        """
        Create a list of contacts.
        see more: https://resend.com/docs/api-reference/audiences/create-audience

        Args:
            params (CreateParams): The audience creation parameters

        Returns:
            CreateAudienceResponse: The created audience response
        """

        path = "/audiences"
        resp = request.Request[Audiences.CreateAudienceResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of audiences.
        see more: https://resend.com/docs/api-reference/audiences/list-audiences

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of audiences to retrieve (max 100, min 1).
                  If not provided, all audiences will be returned without pagination.
                - after: ID after which to retrieve more audiences
                - before: ID before which to retrieve more audiences

        Returns:
            ListResponse: A list of audience objects
        """
        base_path = "/audiences"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Audiences.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str) -> Audience:
        """
        Retrieve a single audience.
        see more: https://resend.com/docs/api-reference/audiences/get-audience

        Args:
            id (str): The audience ID

        Returns:
            Audience: The audience object
        """
        path = f"/audiences/{id}"
        resp = request.Request[Audience](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, id: str) -> RemoveAudienceResponse:
        """
        Delete a single audience.
        see more: https://resend.com/docs/api-reference/audiences/delete-audience

        Args:
            id (str): The audience ID

        Returns:
            RemoveAudienceResponse: The removed audience response
        """
        path = f"/audiences/{id}"
        resp = request.Request[Audiences.RemoveAudienceResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
