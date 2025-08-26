from typing import Any, Dict, List, cast

from typing_extensions import TypedDict

from resend import request

from ._audience import Audience

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


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

    class ListResponse(TypedDict):
        """
        ListResponse type that wraps a list of audience objects

        Attributes:
            object (str): The object type, "list"
            data (List[Audience]): A list of audience objects
        """

        object: str
        """
        The object type, "list"
        """
        data: List[Audience]
        """
        A list of audience objects
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
    def list(cls) -> ListResponse:
        """
        Retrieve a list of audiences.
        see more: https://resend.com/docs/api-reference/audiences/list-audiences

        Returns:
            ListResponse: A list of audience objects
        """
        path = "/audiences/"
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

    @classmethod
    async def create_async(cls, params: CreateParams) -> Audience:
        """
        Create a list of contacts (async).
        see more: https://resend.com/docs/api-reference/audiences/create-audience

        Args:
            params (CreateParams): The audience creation parameters

        Returns:
            Audience: The new audience object
        """
        path = "/audiences"
        resp = await AsyncRequest[Audience](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls) -> ListResponse:
        """
        Retrieve a list of audiences (async).
        see more: https://resend.com/docs/api-reference/audiences/list-audiences

        Returns:
            ListResponse: A list of audience objects
        """
        path = "/audiences/"
        resp = await AsyncRequest[_ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, id: str) -> Audience:
        """
        Retrieve a single audience (async).
        see more: https://resend.com/docs/api-reference/audiences/get-audience

        Args:
            id (str): The audience ID

        Returns:
            Audience: The audience object
        """
        path = f"/audiences/{id}"
        resp = await AsyncRequest[Audience](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, id: str) -> Audience:
        """
        Delete a single audience (async).
        see more: https://resend.com/docs/api-reference/audiences/delete-audience

        Args:
            id (str): The audience ID

        Returns:
            Audience: The audience object
        """
        path = f"/audiences/{id}"
        resp = await AsyncRequest[Audience](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
