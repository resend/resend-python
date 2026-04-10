from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper

from ._automation import (Automation, AutomationConnection, AutomationListItem,
                          AutomationRun, AutomationRunListItem,
                          AutomationStatus, AutomationStep)

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class Automations:

    class CreateParams(TypedDict):
        """
        CreateParams is the class that wraps the parameters for the create method.

        Attributes:
            name (str): The name of the automation
            steps (List[AutomationStep]): The automation workflow steps (must include at least one trigger)
            connections (List[AutomationConnection]): Connections between steps in the automation graph
            status (NotRequired[AutomationStatus]): Initial status, defaults to "disabled"
        """

        name: str
        """
        The name of the automation.
        """
        steps: List[AutomationStep]
        """
        The automation workflow steps. Must include at least one trigger step.
        """
        connections: List[AutomationConnection]
        """
        Connections between steps in the automation graph.
        """
        status: NotRequired[AutomationStatus]
        """
        Initial status of the automation. Defaults to "disabled".
        """

    class UpdateParams(TypedDict):
        """
        UpdateParams is the class that wraps the parameters for the update method.

        Attributes:
            automation_id (str): The ID of the automation to update
            name (NotRequired[str]): Updated automation name
            status (NotRequired[AutomationStatus]): Updated status
            steps (NotRequired[List[AutomationStep]]): Updated steps (must be provided together with connections)
            connections (NotRequired[List[AutomationConnection]]): Updated connections (must be provided together with steps)
        """

        automation_id: str
        """
        The ID of the automation to update.
        """
        name: NotRequired[str]
        """
        Updated automation name.
        """
        status: NotRequired[AutomationStatus]
        """
        Updated status.
        """
        steps: NotRequired[List[AutomationStep]]
        """
        Updated workflow steps. Must be provided together with connections.
        """
        connections: NotRequired[List[AutomationConnection]]
        """
        Updated connections. Must be provided together with steps.
        """

    class ListParams(TypedDict):
        """
        ListParams is the class that wraps the parameters for the list method.

        Attributes:
            status (NotRequired[AutomationStatus]): Filter automations by status
            limit (NotRequired[int]): Number of automations to retrieve (max 100, min 1)
            after (NotRequired[str]): Return items after this cursor
            before (NotRequired[str]): Return items before this cursor
        """

        status: NotRequired[AutomationStatus]
        """
        Filter automations by status.
        """
        limit: NotRequired[int]
        """
        Number of automations to retrieve. Maximum is 100, and minimum is 1.
        """
        after: NotRequired[str]
        """
        Return items after this cursor (for pagination).
        Cannot be used with the before parameter.
        """
        before: NotRequired[str]
        """
        Return items before this cursor (for pagination).
        Cannot be used with the after parameter.
        """

    class CreateResponse(BaseResponse):
        """
        CreateResponse is the class that wraps the response of the create method.

        Attributes:
            object (str): The object type, always "automation"
            id (str): The ID of the created automation
        """

        object: str
        """
        The object type, always "automation".
        """
        id: str
        """
        The ID of the created automation.
        """

    class UpdateResponse(BaseResponse):
        """
        UpdateResponse is the class that wraps the response of the update method.

        Attributes:
            object (str): The object type, always "automation"
            id (str): The ID of the updated automation
        """

        object: str
        """
        The object type, always "automation".
        """
        id: str
        """
        The ID of the updated automation.
        """

    class DeleteResponse(BaseResponse):
        """
        DeleteResponse is the class that wraps the response of the remove method.

        Attributes:
            object (str): The object type, always "automation"
            id (str): The ID of the deleted automation
            deleted (bool): Whether the automation was successfully deleted
        """

        object: str
        """
        The object type, always "automation".
        """
        id: str
        """
        The ID of the deleted automation.
        """
        deleted: bool
        """
        Whether the automation was successfully deleted.
        """

    class StopResponse(BaseResponse):
        """
        StopResponse is the class that wraps the response of the stop method.

        Attributes:
            object (str): The object type, always "automation"
            id (str): The ID of the stopped automation
            status (str): The status after stopping
        """

        object: str
        """
        The object type, always "automation".
        """
        id: str
        """
        The ID of the stopped automation.
        """
        status: str
        """
        The status after stopping.
        """

    class ListResponse(BaseResponse):
        """
        ListResponse is the class that wraps the response of the list method.

        Attributes:
            object (str): The object type, always "list"
            data (List[AutomationListItem]): A list of automation objects
            has_more (bool): Whether there are more results available
        """

        object: str
        """
        The object type, always "list".
        """
        data: List[AutomationListItem]
        """
        A list of automation objects.
        """
        has_more: bool
        """
        Whether there are more results available for pagination.
        """

    class Runs:
        """
        Sub-namespace for automation run methods.
        Accessible as resend.Automations.Runs.
        """

        class ListParams(TypedDict):
            """
            ListParams is the class that wraps the parameters for the list method.

            Attributes:
                status (NotRequired[str]): Comma-separated filter values: "running", "completed", "failed", "cancelled"
                limit (NotRequired[int]): Number of runs to retrieve (max 100, min 1)
                after (NotRequired[str]): Return items after this cursor
                before (NotRequired[str]): Return items before this cursor
            """

            status: NotRequired[str]
            """
            Comma-separated filter values. Valid values: "running", "completed", "failed", "cancelled".
            """
            limit: NotRequired[int]
            """
            Number of runs to retrieve. Maximum is 100, and minimum is 1.
            """
            after: NotRequired[str]
            """
            Return items after this cursor (for pagination).
            Cannot be used with the before parameter.
            """
            before: NotRequired[str]
            """
            Return items before this cursor (for pagination).
            Cannot be used with the after parameter.
            """

        class ListResponse(BaseResponse):
            """
            ListResponse is the class that wraps the response of the list method.

            Attributes:
                object (str): The object type, always "list"
                data (List[AutomationRunListItem]): A list of automation run objects
                has_more (bool): Whether there are more results available
            """

            object: str
            """
            The object type, always "list".
            """
            data: List[AutomationRunListItem]
            """
            A list of automation run objects.
            """
            has_more: bool
            """
            Whether there are more results available for pagination.
            """

        @classmethod
        def list(
            cls,
            automation_id: str,
            params: Optional["Automations.Runs.ListParams"] = None,
        ) -> "Automations.Runs.ListResponse":
            """
            Retrieve a list of runs for an automation.
            see more: https://resend.com/docs/api-reference/automations/list-automation-runs

            Args:
                automation_id (str): The automation ID
                params (Optional[ListParams]): Optional filter and pagination parameters
                    - status: Comma-separated filter values: "running", "completed", "failed", "cancelled"
                    - limit: Number of runs to retrieve (max 100, min 1)
                    - after: Return items after this cursor
                    - before: Return items before this cursor

            Returns:
                ListResponse: A list of automation run objects
            """
            base_path = f"/automations/{automation_id}/runs"
            query_params = cast(Dict[Any, Any], params) if params else None
            path = PaginationHelper.build_paginated_path(base_path, query_params)
            resp = request.Request[Automations.Runs.ListResponse](
                path=path, params={}, verb="get"
            ).perform_with_content()
            return resp

        @classmethod
        def get(cls, automation_id: str, run_id: str) -> AutomationRun:
            """
            Retrieve a single automation run.
            see more: https://resend.com/docs/api-reference/automations/get-automation-run

            Args:
                automation_id (str): The automation ID
                run_id (str): The run ID

            Returns:
                AutomationRun: The automation run object
            """
            path = f"/automations/{automation_id}/runs/{run_id}"
            resp = request.Request[AutomationRun](
                path=path, params={}, verb="get"
            ).perform_with_content()
            return resp

        @classmethod
        async def list_async(
            cls,
            automation_id: str,
            params: Optional["Automations.Runs.ListParams"] = None,
        ) -> "Automations.Runs.ListResponse":
            """
            Retrieve a list of runs for an automation (async).
            see more: https://resend.com/docs/api-reference/automations/list-automation-runs

            Args:
                automation_id (str): The automation ID
                params (Optional[ListParams]): Optional filter and pagination parameters
                    - status: Comma-separated filter values: "running", "completed", "failed", "cancelled"
                    - limit: Number of runs to retrieve (max 100, min 1)
                    - after: Return items after this cursor
                    - before: Return items before this cursor

            Returns:
                ListResponse: A list of automation run objects
            """
            base_path = f"/automations/{automation_id}/runs"
            query_params = cast(Dict[Any, Any], params) if params else None
            path = PaginationHelper.build_paginated_path(base_path, query_params)
            resp = await AsyncRequest[Automations.Runs.ListResponse](
                path=path, params={}, verb="get"
            ).perform_with_content()
            return resp

        @classmethod
        async def get_async(cls, automation_id: str, run_id: str) -> AutomationRun:
            """
            Retrieve a single automation run (async).
            see more: https://resend.com/docs/api-reference/automations/get-automation-run

            Args:
                automation_id (str): The automation ID
                run_id (str): The run ID

            Returns:
                AutomationRun: The automation run object
            """
            path = f"/automations/{automation_id}/runs/{run_id}"
            resp = await AsyncRequest[AutomationRun](
                path=path, params={}, verb="get"
            ).perform_with_content()
            return resp

    @classmethod
    def create(cls, params: "Automations.CreateParams") -> "Automations.CreateResponse":
        """
        Create an automation.
        see more: https://resend.com/docs/api-reference/automations/create-automation

        Args:
            params (CreateParams): The automation creation parameters

        Returns:
            CreateResponse: The created automation response
        """
        path = "/automations"
        resp = request.Request[Automations.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, automation_id: str) -> Automation:
        """
        Retrieve a single automation.
        see more: https://resend.com/docs/api-reference/automations/get-automation

        Args:
            automation_id (str): The automation ID

        Returns:
            Automation: The automation object
        """
        path = f"/automations/{automation_id}"
        resp = request.Request[Automation](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: "Automations.UpdateParams") -> "Automations.UpdateResponse":
        """
        Update an automation.
        see more: https://resend.com/docs/api-reference/automations/update-automation

        Args:
            params (UpdateParams): The automation update parameters

        Returns:
            UpdateResponse: The updated automation response
        """
        path = f"/automations/{params['automation_id']}"
        body = {k: v for k, v in params.items() if k != "automation_id"}
        resp = request.Request[Automations.UpdateResponse](
            path=path, params=cast(Dict[Any, Any], body), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, automation_id: str) -> "Automations.DeleteResponse":
        """
        Delete an automation.
        see more: https://resend.com/docs/api-reference/automations/delete-automation

        Args:
            automation_id (str): The automation ID

        Returns:
            DeleteResponse: The delete response
        """
        path = f"/automations/{automation_id}"
        resp = request.Request[Automations.DeleteResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    def stop(cls, automation_id: str) -> "Automations.StopResponse":
        """
        Stop all active runs of an automation.
        see more: https://resend.com/docs/api-reference/automations/stop-automation

        Args:
            automation_id (str): The automation ID

        Returns:
            StopResponse: The stop response
        """
        path = f"/automations/{automation_id}/stop"
        resp = request.Request[Automations.StopResponse](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def list(
        cls, params: Optional["Automations.ListParams"] = None
    ) -> "Automations.ListResponse":
        """
        Retrieve a list of automations.
        see more: https://resend.com/docs/api-reference/automations/list-automations

        Args:
            params (Optional[ListParams]): Optional filter and pagination parameters
                - status: Filter automations by status ("enabled" or "disabled")
                - limit: Number of automations to retrieve (max 100, min 1)
                - after: Return items after this cursor
                - before: Return items before this cursor

        Returns:
            ListResponse: A list of automation objects
        """
        base_path = "/automations"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Automations.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def create_async(
        cls, params: "Automations.CreateParams"
    ) -> "Automations.CreateResponse":
        """
        Create an automation (async).
        see more: https://resend.com/docs/api-reference/automations/create-automation

        Args:
            params (CreateParams): The automation creation parameters

        Returns:
            CreateResponse: The created automation response
        """
        path = "/automations"
        resp = await AsyncRequest[Automations.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, automation_id: str) -> Automation:
        """
        Retrieve a single automation (async).
        see more: https://resend.com/docs/api-reference/automations/get-automation

        Args:
            automation_id (str): The automation ID

        Returns:
            Automation: The automation object
        """
        path = f"/automations/{automation_id}"
        resp = await AsyncRequest[Automation](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(
        cls, params: "Automations.UpdateParams"
    ) -> "Automations.UpdateResponse":
        """
        Update an automation (async).
        see more: https://resend.com/docs/api-reference/automations/update-automation

        Args:
            params (UpdateParams): The automation update parameters

        Returns:
            UpdateResponse: The updated automation response
        """
        path = f"/automations/{params['automation_id']}"
        body = {k: v for k, v in params.items() if k != "automation_id"}
        resp = await AsyncRequest[Automations.UpdateResponse](
            path=path, params=cast(Dict[Any, Any], body), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def remove_async(cls, automation_id: str) -> "Automations.DeleteResponse":
        """
        Delete an automation (async).
        see more: https://resend.com/docs/api-reference/automations/delete-automation

        Args:
            automation_id (str): The automation ID

        Returns:
            DeleteResponse: The delete response
        """
        path = f"/automations/{automation_id}"
        resp = await AsyncRequest[Automations.DeleteResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp

    @classmethod
    async def stop_async(cls, automation_id: str) -> "Automations.StopResponse":
        """
        Stop all active runs of an automation (async).
        see more: https://resend.com/docs/api-reference/automations/stop-automation

        Args:
            automation_id (str): The automation ID

        Returns:
            StopResponse: The stop response
        """
        path = f"/automations/{automation_id}/stop"
        resp = await AsyncRequest[Automations.StopResponse](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    async def list_async(
        cls, params: Optional["Automations.ListParams"] = None
    ) -> "Automations.ListResponse":
        """
        Retrieve a list of automations (async).
        see more: https://resend.com/docs/api-reference/automations/list-automations

        Args:
            params (Optional[ListParams]): Optional filter and pagination parameters
                - status: Filter automations by status ("enabled" or "disabled")
                - limit: Number of automations to retrieve (max 100, min 1)
                - after: Return items after this cursor
                - before: Return items before this cursor

        Returns:
            ListResponse: A list of automation objects
        """
        base_path = "/automations"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = await AsyncRequest[Automations.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp
