from typing import Any, Dict, List, cast

from typing_extensions import Literal, TypedDict

from resend import request

from ._audience import Audience, AudienceObject, ShortAudience


class _ListResponse(TypedDict):
    object: Literal["list"]
    """
    The object type
    """
    data: List[ShortAudience]
    """
    A list of audience objects
    """


class _CreateResponse(TypedDict):
    object: AudienceObject
    """
    The object type
    """
    id: str
    """
    The unique identifier of the audience.
    """
    name: str
    """
    The name of the audience.
    """


class _RemoveResponse(TypedDict):
    object: AudienceObject
    """
    The object type
    """
    id: str
    """
    The unique identifier of the audience.
    """
    deleted: bool
    """
    Whether the audience was deleted.
    """


class Audiences:

    class CreateResponse(_CreateResponse):
        """
        Class that wraps the response of the create audience endpoint

        Attributes:
            object (str): The object type
            id (str): The audience ID
            name (str): The audience name
        """

    class ListResponse(_ListResponse):
        """
        ListResponse type that wraps a list of audience objects

        Attributes:
            object (str): The object type
            data (List[ShortAudience]): A list of audience objects
        """

    class RemoveResponse(_RemoveResponse):
        """
        Class that wraps the response of the remove audience endpoint

        Attributes:
            object (str): The object type
            id (str): The audience ID
            deleted (bool): Whether the audience was deleted
        """

    class CreateParams(TypedDict):
        name: str
        """
        The name of the audience.
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateResponse:
        """
        Create a list of contacts.
        see more: https://resend.com/docs/api-reference/audiences/create-audience

        Args:
            params (CreateParams): The audience creation parameters

        Returns:
            Audience: The new audience object
        """
        path = "/audiences"
        resp = request.Request[_CreateResponse](
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
        resp = request.Request[_ListResponse](
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
    def remove(cls, id: str) -> RemoveResponse:
        """
        Delete a single audience.
        see more: https://resend.com/docs/api-reference/audiences/delete-audience

        Args:
            id (str): The audience ID

        Returns:
            Audience: The audience object
        """
        path = f"/audiences/{id}"
        resp = request.Request[_RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
