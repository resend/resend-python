from typing import List, Optional

from typing_extensions import Literal

from resend._base_response import BaseResponse

InboxAgentAction = Literal[
    "draft_reply",
    "forward_thread",
    "add_labels",
    "assign_thread",
    "mark_as_spam",
    "archive_thread",
    "delete_thread",
]
"""
An action the inbox agent can take.
"""


class InboxAgentSettings(BaseResponse):
    """
    InboxAgentSettings are the agent settings of an inbox.
    """

    object: str
    """
    The object type. Always ``inbox_agent``.
    """
    instructions: Optional[str]
    """
    Instructions the agent follows when it handles the threads of the inbox.
    None when no instructions are set.
    """
    tone: Optional[str]
    """
    The tone the agent writes in, such as ``friendly and concise``.
    None when no tone is set.
    """
    enabled_actions: List[InboxAgentAction]
    """
    The actions the agent can take. Empty when no actions are enabled.
    """
