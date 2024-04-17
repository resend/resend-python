from typing import Any, Dict, List, cast

from typing_extensions import TypedDict

from resend import request

from ._audience import Audience


class Audiences:
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
        """
        path = "/audiences"
        return Audience.new_from_request(
            request.Request(
                path=path, params=cast(Dict[Any, Any], params), verb="post"
            ).perform()
        )

    @classmethod
    def list(cls) -> List[Audience]:
        """
        Retrieve a list of audiences.
        see more: https://resend.com/docs/api-reference/audiences/list-audiences
        """
        path = "/audiences/"
        resp = request.Request(path=path, params={}, verb="get").perform()
        return (
            [Audience.new_from_request(aud) for aud in resp["data"]]
            if "data" in resp
            else []
        )

    @classmethod
    def get(cls, id: str) -> Audience:
        """
        Retrieve a single audience.
        see more: https://resend.com/docs/api-reference/audiences/get-audience
        """
        path = f"/audiences/{id}"
        return Audience.new_from_request(
            request.Request(path=path, params={}, verb="get").perform()
        )

    @classmethod
    def remove(cls, id: str) -> Audience:
        """
        Delete a single audience.
        see more: https://resend.com/docs/api-reference/audiences/delete-audience
        """
        path = f"/audiences/{id}"
        return Audience.new_from_request(
            request.Request(path=path, params={}, verb="delete").perform()
        )
