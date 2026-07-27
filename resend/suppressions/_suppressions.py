from typing import Any, Dict, List, Optional, cast
from urllib.parse import quote

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper
from resend.suppressions.batch._suppressions_batch import SuppressionsBatch

from ._suppression import Suppression, SuppressionListItem, SuppressionOrigin

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class Suppressions:

    class Batch(SuppressionsBatch):
        pass

    class AddSuppressionResponse(BaseResponse):
        """
        AddSuppressionResponse wraps the response of a created suppression.

        Attributes:
            object (str): Always 'suppression'.
            id (str): The ID of the created suppression.
        """

        object: str
        id: str

    class RemoveSuppressionResponse(BaseResponse):
        """
        RemoveSuppressionResponse wraps the response of a removed suppression.

        Attributes:
            object (str): Always 'suppression'.
            id (str): The ID of the removed suppression.
            deleted (bool): Whether the suppression was deleted.
        """

        object: str
        id: str
        deleted: bool

    class ListResponse(BaseResponse):
        """
        ListResponse wraps a paginated list of suppressions.

        Attributes:
            object (str): Always 'list'.
            data (List[SuppressionListItem]): The list of suppression entries.
            has_more (bool): Whether additional pages of results exist.
        """

        object: str
        data: List[SuppressionListItem]
        has_more: bool

    class AddParams(TypedDict):
        email: str
        """
        The email address to suppress.
        """

    class ListParams(TypedDict):
        origin: NotRequired[SuppressionOrigin]
        """
        Filter suppressions by origin: 'bounce', 'complaint' or 'manual'.
        """
        limit: NotRequired[int]
        """
        Number of suppressions to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        The ID after which we'll retrieve more suppressions (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        The ID before which we'll retrieve more suppressions (for pagination).
        This ID will not be included in the returned list.
        Cannot be used with the after parameter.
        """

    @classmethod
    def add(cls, params: AddParams) -> AddSuppressionResponse:
        """
        Add an email address to the suppression list. The address is normalized
        server-side, and adding an already-suppressed address returns the existing
        suppression rather than an error.
        see more: https://resend.com/docs/api-reference/suppressions/add-suppression

        Args:
            params (AddParams): The suppression parameters

        Returns:
            AddSuppressionResponse: The created suppression response
        """
        path = "/suppressions"
        resp = request.Request[Suppressions.AddSuppressionResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of suppressions.
        see more: https://resend.com/docs/api-reference/suppressions/list-suppressions

        Args:
            params (Optional[ListParams]): Optional filtering and pagination parameters

        Returns:
            ListResponse: A paginated list of suppression objects
        """
        base_path = "/suppressions"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Suppressions.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id_or_email: str) -> Suppression:
        """
        Retrieve a single suppression by ID or by email address. Returns a
        not_found error if the address is not suppressed.
        see more: https://resend.com/docs/api-reference/suppressions/get-suppression

        Args:
            id_or_email (str): The suppression ID or the suppressed email address

        Returns:
            Suppression: The suppression object
        """
        if not id_or_email:
            raise ValueError("id or email must be provided")

        path = f"/suppressions/{quote(id_or_email, safe='')}"
        resp = request.Request[Suppression](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, id_or_email: str) -> RemoveSuppressionResponse:
        """
        Remove a single suppression by ID or by email address. Returns a
        not_found error if the address is not suppressed.
        see more: https://resend.com/docs/api-reference/suppressions/remove-suppression

        Args:
            id_or_email (str): The suppression ID or the suppressed email address

        Returns:
            RemoveSuppressionResponse: The removed suppression response
        """
        if not id_or_email:
            raise ValueError("id or email must be provided")

        path = f"/suppressions/{quote(id_or_email, safe='')}"
        resp = request.Request[Suppressions.RemoveSuppressionResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def add_async(cls, params: AddParams) -> AddSuppressionResponse:
        """
        Add an email address to the suppression list (async). The address is
        normalized server-side, and adding an already-suppressed address returns
        the existing suppression rather than an error.
        see more: https://resend.com/docs/api-reference/suppressions/add-suppression

        Args:
            params (AddParams): The suppression parameters

        Returns:
            AddSuppressionResponse: The created suppression response
        """
        path = "/suppressions"
        resp = await AsyncRequest[Suppressions.AddSuppressionResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, params: Optional[ListParams] = None) -> ListResponse:
        """
        Retrieve a list of suppressions (async).
        see more: https://resend.com/docs/api-reference/suppressions/list-suppressions

        Args:
            params (Optional[ListParams]): Optional filtering and pagination parameters

        Returns:
            ListResponse: A paginated list of suppression objects
        """
        base_path = "/suppressions"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = await AsyncRequest[Suppressions.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, id_or_email: str) -> Suppression:
        """
        Retrieve a single suppression by ID or by email address (async). Returns
        a not_found error if the address is not suppressed.
        see more: https://resend.com/docs/api-reference/suppressions/get-suppression

        Args:
            id_or_email (str): The suppression ID or the suppressed email address

        Returns:
            Suppression: The suppression object
        """
        if not id_or_email:
            raise ValueError("id or email must be provided")

        path = f"/suppressions/{quote(id_or_email, safe='')}"
        resp = await AsyncRequest[Suppression](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, id_or_email: str) -> RemoveSuppressionResponse:
        """
        Remove a single suppression by ID or by email address (async). Returns a
        not_found error if the address is not suppressed.
        see more: https://resend.com/docs/api-reference/suppressions/remove-suppression

        Args:
            id_or_email (str): The suppression ID or the suppressed email address

        Returns:
            RemoveSuppressionResponse: The removed suppression response
        """
        if not id_or_email:
            raise ValueError("id or email must be provided")

        path = f"/suppressions/{quote(id_or_email, safe='')}"
        resp = await AsyncRequest[Suppressions.RemoveSuppressionResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
