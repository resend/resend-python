import warnings
from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from resend._base_response import BaseResponse
from resend.segments._segments import Segments

from ._audience import Audience


class Audiences:

    class RemoveAudienceResponse(BaseResponse):
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

    class ListResponse(BaseResponse):
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

    class CreateAudienceResponse(BaseResponse):
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

        .. deprecated::
            Use Segments.create() instead. Audiences is now an alias for Segments.
        """
        warnings.warn(
            "Audiences is deprecated. Use Segments instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return Segments.create(params)

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

        .. deprecated::
            Use Segments.list() instead. Audiences is now an alias for Segments.
        """
        warnings.warn(
            "Audiences is deprecated. Use Segments instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return Segments.list(params)

    @classmethod
    def get(cls, id: str) -> Audience:
        """
        Retrieve a single audience.
        see more: https://resend.com/docs/api-reference/audiences/get-audience

        Args:
            id (str): The audience ID

        Returns:
            Audience: The audience object

        .. deprecated::
            Use Segments.get() instead. Audiences is now an alias for Segments.
        """
        warnings.warn(
            "Audiences is deprecated. Use Segments instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return Segments.get(id)

    @classmethod
    def remove(cls, id: str) -> RemoveAudienceResponse:
        """
        Delete a single audience.
        see more: https://resend.com/docs/api-reference/audiences/delete-audience

        Args:
            id (str): The audience ID

        Returns:
            RemoveAudienceResponse: The removed audience response

        .. deprecated::
            Use Segments.remove() instead. Audiences is now an alias for Segments.
        """
        warnings.warn(
            "Audiences is deprecated. Use Segments instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return Segments.remove(id)
