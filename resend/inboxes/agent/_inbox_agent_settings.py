from typing import List, Optional

from typing_extensions import Literal

from resend._base_response import BaseResponse

InboxAgentAction = Literal[
    "draft_reply",
    "forward_thread",
    "add_labels",
    "assign_thread",
    "mark_as_spam",
    "archive",
    "move_to_trash",
]
"""
An action the inbox agent can take.
"""

InboxAgentTone = Literal[
    "concise_professional",
    "concise_casual",
    "expanded_professional",
    "expanded_casual",
]
"""
A tone preset the inbox agent writes in.
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
    tone: Optional[InboxAgentTone]
    """
    The tone the agent writes in. None when no tone is set.
    """
    actions: List[InboxAgentAction]
    """
    The actions the agent can take. Empty when no actions are enabled.
    """
