import json as json_lib
from typing import Any, Dict, List, Optional, cast

from typing_extensions import Literal, NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper

from ._contact_import import ContactImport

try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class ContactImports:
    class CreateContactImportResponse(BaseResponse):
        """
        CreateContactImportResponse wraps the response from a successful import creation.

        Attributes:
            object (str): Always 'contact_import'.
            id (str): Unique identifier for the created import job.
        """

        object: str
        id: str

    class ListContactImportsResponse(BaseResponse):
        """
        ListContactImportsResponse wraps a paginated list of contact imports.

        Attributes:
            object (str): Always 'list'.
            data (List[ContactImport]): The list of import objects.
            has_more (bool): Whether additional pages of results exist.
        """

        object: str
        data: List[ContactImport]
        has_more: bool

    class CreateParams(TypedDict):
        file: bytes
        """
        CSV file content to import. Maximum size is 50MB. (required)
        """
        filename: NotRequired[str]
        """
        Filename used in the multipart upload. Defaults to 'import.csv'.
        """
        column_map: NotRequired[Dict[str, Any]]
        """
        Maps contact fields and custom property keys to CSV column names.
        Will be JSON-encoded before sending.
        Example: {"email": "Email", "first_name": "First Name"}
        """
        on_conflict: NotRequired[Literal["upsert", "skip"]]
        """
        Strategy when an imported contact already exists: 'upsert' or 'skip' (default 'skip').
        """
        segments: NotRequired[List[str]]
        """
        List of segment IDs to add imported contacts to.
        Will be serialized as [{"id": "..."}] before sending.
        """
        topics: NotRequired[List[Dict[str, str]]]
        """
        List of topic subscriptions for imported contacts.
        Each entry must have 'id' and 'subscription' ('opt_in' or 'opt_out').
        """

    class ListParams(TypedDict):
        status: NotRequired[Literal["queued", "in_progress", "completed", "failed"]]
        """
        Filter imports by status.
        """
        limit: NotRequired[int]
        """
        Number of imports to retrieve. Maximum is 100.
        """
        after: NotRequired[str]
        """
        Cursor for forward pagination (exclusive).
        """
        before: NotRequired[str]
        """
        Cursor for backward pagination (exclusive).
        """

    @classmethod
    def create(cls, params: CreateParams) -> CreateContactImportResponse:
        """
        Create a new contact import from a CSV file.
        see more: https://resend.com/docs/api-reference/contacts/create-contact-import

        Args:
            params (CreateParams): Import parameters including the CSV file content.

        Returns:
            CreateContactImportResponse: The created import job with its ID.
        """
        if not params.get("file"):
            raise ValueError("file is required")

        filename = params.get("filename", "import.csv")
        files: Dict[str, Any] = {
            "file": (filename, params["file"], "text/csv"),
        }
        form_data: Dict[str, str] = {}
        if "column_map" in params:
            form_data["column_map"] = json_lib.dumps(params["column_map"])
        if "on_conflict" in params:
            form_data["on_conflict"] = params["on_conflict"]
        if "segments" in params:
            form_data["segments"] = json_lib.dumps(
                [{"id": sid} for sid in params["segments"]]
            )
        if "topics" in params:
            form_data["topics"] = json_lib.dumps(params["topics"])

        resp = request.Request[ContactImports.CreateContactImportResponse](
            path="/contacts/imports",
            params={},
            verb="post",
            files=files,
            data=form_data,
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, id: str) -> ContactImport:
        """
        Retrieve a single contact import by ID.
        see more: https://resend.com/docs/api-reference/contacts/get-contact-import

        Args:
            id (str): The contact import ID.

        Returns:
            ContactImport: The contact import object.
        """
        if not id:
            raise ValueError("id is required")

        resp = request.Request[ContactImport](
            path=f"/contacts/imports/{id}",
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListContactImportsResponse:
        """
        Retrieve a list of contact imports.
        see more: https://resend.com/docs/api-reference/contacts/list-contact-imports

        Args:
            params (Optional[ListParams]): Optional filtering and pagination parameters.

        Returns:
            ListContactImportsResponse: Paginated list of contact import objects.
        """
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path("/contacts/imports", query_params)
        # Append status filter if provided (PaginationHelper only handles limit/after/before)
        if params and "status" in params:
            separator = "&" if "?" in path else "?"
            path = f"{path}{separator}status={params['status']}"

        resp = request.Request[ContactImports.ListContactImportsResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(cls, params: CreateParams) -> CreateContactImportResponse:
        """
        Create a new contact import from a CSV file (async).
        see more: https://resend.com/docs/api-reference/contacts/create-contact-import

        Args:
            params (CreateParams): Import parameters including the CSV file content.

        Returns:
            CreateContactImportResponse: The created import job with its ID.
        """
        if not params.get("file"):
            raise ValueError("file is required")

        filename = params.get("filename", "import.csv")
        files: Dict[str, Any] = {
            "file": (filename, params["file"], "text/csv"),
        }
        form_data: Dict[str, str] = {}
        if "column_map" in params:
            form_data["column_map"] = json_lib.dumps(params["column_map"])
        if "on_conflict" in params:
            form_data["on_conflict"] = params["on_conflict"]
        if "segments" in params:
            form_data["segments"] = json_lib.dumps(
                [{"id": sid} for sid in params["segments"]]
            )
        if "topics" in params:
            form_data["topics"] = json_lib.dumps(params["topics"])

        resp = await AsyncRequest[ContactImports.CreateContactImportResponse](
            path="/contacts/imports",
            params={},
            verb="post",
            files=files,
            data=form_data,
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, id: str) -> ContactImport:
        """
        Retrieve a single contact import by ID (async).
        see more: https://resend.com/docs/api-reference/contacts/get-contact-import

        Args:
            id (str): The contact import ID.

        Returns:
            ContactImport: The contact import object.
        """
        if not id:
            raise ValueError("id is required")

        resp = await AsyncRequest[ContactImport](
            path=f"/contacts/imports/{id}",
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(cls, params: Optional[ListParams] = None) -> ListContactImportsResponse:
        """
        Retrieve a list of contact imports (async).
        see more: https://resend.com/docs/api-reference/contacts/list-contact-imports

        Args:
            params (Optional[ListParams]): Optional filtering and pagination parameters.

        Returns:
            ListContactImportsResponse: Paginated list of contact import objects.
        """
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path("/contacts/imports", query_params)
        if params and "status" in params:
            separator = "&" if "?" in path else "?"
            path = f"{path}{separator}status={params['status']}"

        resp = await AsyncRequest[ContactImports.ListContactImportsResponse](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp
