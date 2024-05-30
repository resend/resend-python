from typing import Any, Dict, List, cast

from typing_extensions import TypedDict

from resend import request

from ._audience import Audience


class _ListResponse(TypedDict):
    data: List[Audience]
    """
    A list of audience objects
    """


class Audiences:

    class ListResponse(_ListResponse):
        """
        ListResponse type that wraps a list of audience objects

        Attributes:
            data (List[Audience]): A list of audience objects
        """

    class CreateParams(TypedDict):
        name: str
        """
        The name of the audience.
        """

    @classmethod
    def create(cls, params: CreateParams) -> Audience:
        """
        Create a list of contacts.
        see more: https://resend.com/docs/api-reference/audiences/create-audience

        Args:
            params (CreateParams): The audience creation parameters

        Returns:
            Audience: The new audience object
        """
        path = "/audiences"
        resp = request.Request[Audience](
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
    def remove(cls, id: str) -> Audience:
        """
        Delete a single audience.
        see more: https://resend.com/docs/api-reference/audiences/delete-audience

        Args:
            id (str): The audience ID

        Returns:
            Audience: The audience object
        """
        path = f"/audiences/{id}"
        resp = request.Request[Audience](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
