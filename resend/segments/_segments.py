from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend.pagination_helper import PaginationHelper

from ._segment import Segment


class Segments:

    class RemoveSegmentResponse(TypedDict):
        """
        RemoveSegmentResponse is the type that wraps the response of the segment that was removed

        Attributes:
            object (str): The object type, "audience"
            id (str): The ID of the removed segment
            deleted (bool): Whether the segment was deleted
        """

        object: str
        """
        The object type, "audience"
        """
        id: str
        """
        The ID of the removed segment
        """
        deleted: bool
        """
        Whether the segment was deleted
        """

    class ListParams(TypedDict):
        limit: NotRequired[int]
        """
        Number of segments to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more segments (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more segments (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of segment objects with pagination metadata

        Attributes:
            object (str): The object type, always "list"
            data (List[Segment]): A list of segment objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list"
        """
        data: List[Segment]
        """
        A list of segment objects
        """
        has_more: bool
        """
        Whether there are more results available for pagination
        """

    class CreateSegmentResponse(TypedDict):
        """
        CreateSegmentResponse is the type that wraps the response of the segment that was created

        Attributes:
            object (str): The object type, "audience"
            id (str): The ID of the created segment
            name (str): The name of the created segment
        """

        object: str
        """
        The object type, "audience"
        """
        id: str
        """
        The ID of the created segment
        """
        name: str
        """
        The name of the created segment
        """

    class CreateParams(TypedDict):
        name: str
        """
        The name of the segment.
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateSegmentResponse:
        """
        Create a segment.
        see more: https://resend.com/docs/api-reference/segments/create-segment

        Args:
            params (CreateParams): The segment creation parameters

        Returns:
            CreateSegmentResponse: The created segment response
        """

        path = "/segments"
        resp = request.Request[Segments.CreateSegmentResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of segments.
        see more: https://resend.com/docs/api-reference/segments/list-segments

        Args:
            params (Optional[ListParams]): Optional pagination parameters
                - limit: Number of segments to retrieve (max 100, min 1).
                  If not provided, all segments will be returned without pagination.
                - after: ID after which to retrieve more segments
                - before: ID before which to retrieve more segments

        Returns:
            ListResponse: A list of segment objects
        """
        base_path = "/segments"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Segments.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str) -> Segment:
        """
        Retrieve a single segment.
        see more: https://resend.com/docs/api-reference/segments/get-segment

        Args:
            id (str): The segment ID

        Returns:
            Segment: The segment object
        """
        path = f"/segments/{id}"
        resp = request.Request[Segment](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, id: str) -> RemoveSegmentResponse:
        """
        Delete a single segment.
        see more: https://resend.com/docs/api-reference/segments/delete-segment

        Args:
            id (str): The segment ID

        Returns:
            RemoveSegmentResponse: The removed segment response
        """
        path = f"/segments/{id}"
        resp = request.Request[Segments.RemoveSegmentResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
