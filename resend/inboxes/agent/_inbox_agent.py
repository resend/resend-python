from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.inboxes._query import without_keys

from ._inbox_agent_settings import InboxAgentAction, InboxAgentSettings

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class InboxAgent:
    """
    InboxAgent manages the agent settings of an inbox.
    """

    class UpdateParams(TypedDict):
        """
        UpdateParams are the parameters for updating the agent settings of an inbox.
        At least one of ``instructions``, ``tone``, or ``enabled_actions`` must be
        provided. Omitted fields keep their current value.

        Attributes:
            inbox_id (str): The Inbox ID. An email address is not accepted.
            instructions (NotRequired[Optional[str]]): Instructions for the agent.
            tone (NotRequired[Optional[str]]): The tone the agent writes in.
            enabled_actions (NotRequired[List[InboxAgentAction]]): The actions the agent can take.
        """

        inbox_id: str
        """
        The Inbox ID. An email address is not accepted.
        """
        instructions: NotRequired[Optional[str]]
        """
        Instructions the agent follows when it handles the threads of the inbox.
        Max 4000 characters. Leading and trailing whitespace is trimmed, and the
        trimmed value must not be empty. Send None to clear the instructions.
        """
        tone: NotRequired[Optional[str]]
        """
        The tone the agent writes in. Use one of the presets
        ``concise_professional``, ``concise_casual``, ``expanded_professional``,
        or ``expanded_casual``, or describe the tone in your own words, such as
        ``friendly and concise``. Custom text is max 64 characters. Leading and
        trailing whitespace is trimmed, and the trimmed value must not be empty.
        Send None to clear the tone.
        """
        enabled_actions: NotRequired[List[InboxAgentAction]]
        """
        The actions the agent can take. Replaces the whole set. Duplicates are
        removed. Send an empty list to disable all actions.
        """

    class UpdateResponse(BaseResponse):
        """
        UpdateResponse is the response of updating the agent settings of an inbox.

        Attributes:
            object (str): The object type. Always "inbox_agent".
            id (str): The ID of the inbox agent.
        """

        object: str
        """
        The object type. Always ``inbox_agent``.
        """
        id: str
        """
        The ID of the inbox agent.
        """

    @classmethod
    def get(cls, inbox_id: str) -> InboxAgentSettings:
        """
        Retrieve the agent settings of an inbox. An inbox without a configured
        agent returns empty settings: ``instructions`` and ``tone`` are None and
        ``enabled_actions`` is an empty list.
        see more: https://resend.com/docs/api-reference/inboxes/get-agent

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.

        Returns:
            InboxAgentSettings: The agent settings of the inbox
        """
        path = f"/inboxes/{inbox_id}/agent"
        resp = request.Request[InboxAgentSettings](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update the agent settings of an inbox. The agent is created when the
        inbox has none. Omitted fields keep their current value.
        see more: https://resend.com/docs/api-reference/inboxes/update-agent

        Args:
            params (UpdateParams): The inbox ID and the settings to change

        Returns:
            UpdateResponse: The object type and the ID of the inbox agent
        """
        path = f"/inboxes/{params['inbox_id']}/agent"
        resp = request.Request[InboxAgent.UpdateResponse](
            path=path, params=without_keys(params, "inbox_id"), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    async def get_async(cls, inbox_id: str) -> InboxAgentSettings:
        """
        Retrieve the agent settings of an inbox (async). An inbox without a
        configured agent returns empty settings: ``instructions`` and ``tone``
        are None and ``enabled_actions`` is an empty list.
        see more: https://resend.com/docs/api-reference/inboxes/get-agent

        Args:
            inbox_id (str): The Inbox ID. An email address is not accepted.

        Returns:
            InboxAgentSettings: The agent settings of the inbox
        """
        path = f"/inboxes/{inbox_id}/agent"
        resp = await AsyncRequest[InboxAgentSettings](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    async def update_async(cls, params: UpdateParams) -> UpdateResponse:
        """
        Update the agent settings of an inbox (async). The agent is created when
        the inbox has none. Omitted fields keep their current value.
        see more: https://resend.com/docs/api-reference/inboxes/update-agent

        Args:
            params (UpdateParams): The inbox ID and the settings to change

        Returns:
            UpdateResponse: The object type and the ID of the inbox agent
        """
        path = f"/inboxes/{params['inbox_id']}/agent"
        resp = await AsyncRequest[InboxAgent.UpdateResponse](
            path=path, params=without_keys(params, "inbox_id"), verb="patch"
        ).perform_with_content()
        return resp
