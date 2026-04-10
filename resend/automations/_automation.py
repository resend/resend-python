from typing import Any, Dict, List, Union

from typing_extensions import Literal, NotRequired, TypedDict

AutomationStatus = Literal["enabled", "disabled"]
AutomationRunStatus = Literal["running", "completed", "failed", "cancelled"]
AutomationStepType = Literal[
    "trigger",
    "send_email",
    "delay",
    "wait_for_event",
    "condition",
    "contact_update",
    "contact_delete",
    "add_to_segment",
]
AutomationConnectionType = Literal[
    "default",
    "condition_met",
    "condition_not_met",
    "timeout",
    "event_received",
]

# Uses functional TypedDict syntax because "from" is a reserved keyword in Python
AutomationConnection = TypedDict(
    "AutomationConnection",
    {
        "from": str,
        "to": str,
        "type": NotRequired[AutomationConnectionType],
    },
)
"""
AutomationConnection represents a connection between two steps in an automation graph.

Attributes:
    from (str): The key of the source step
    to (str): The key of the target step
    type (NotRequired[AutomationConnectionType]): The type of connection, defaults to "default"
"""


class AutomationStep(TypedDict):
    """
    AutomationStep represents a step in an automation workflow request.

    Attributes:
        key (str): Unique identifier for the step within the graph
        type (AutomationStepType): The type of step
        config (Dict[str, Any]): Step-specific configuration object
    """

    key: str
    """
    Unique identifier for the step within the graph.
    """
    type: AutomationStepType
    """
    The type of step.
    """
    config: Dict[str, Any]
    """
    Step-specific configuration. Shape depends on the step type.
    """


class AutomationResponseStep(TypedDict):
    """
    AutomationResponseStep represents a step as returned by the API.

    Attributes:
        key (str): The step identifier
        type (AutomationStepType): The type of step
        config (Any): Step-specific configuration
    """

    key: str
    """
    The step identifier.
    """
    type: AutomationStepType
    """
    The type of step.
    """
    config: Any
    """
    Step-specific configuration.
    """


class AutomationRunStep(TypedDict):
    """
    AutomationRunStep represents a step execution within an automation run.

    Attributes:
        key (str): The step identifier
        type (str): The type of step
        status (str): Execution status of this step
        started_at (Union[str, None]): When the step started executing
        completed_at (Union[str, None]): When the step completed executing
        output (Any): The step output data
        error (Any): Any error that occurred
        created_at (str): When the run step was created
    """

    key: str
    """
    The step identifier.
    """
    type: AutomationStepType
    """
    The type of step.
    """
    status: str
    """
    Execution status of this step.
    """
    started_at: Union[str, None]
    """
    When the step started executing (ISO 8601 format), or None if not started.
    """
    completed_at: Union[str, None]
    """
    When the step completed executing (ISO 8601 format), or None if not completed.
    """
    output: Any
    """
    The step output data.
    """
    error: Any
    """
    Any error that occurred during step execution.
    """
    created_at: str
    """
    When the run step was created (ISO 8601 format).
    """


class AutomationListItem(TypedDict):
    """
    AutomationListItem represents an automation in list responses.

    Attributes:
        id (str): The automation ID
        name (str): The automation name
        status (AutomationStatus): Current status
        created_at (str): Creation date/time
        updated_at (str): Last update date/time
    """

    id: str
    """
    The automation ID.
    """
    name: str
    """
    The automation name.
    """
    status: AutomationStatus
    """
    Current status of the automation.
    """
    created_at: str
    """
    When the automation was created (ISO 8601 format).
    """
    updated_at: str
    """
    When the automation was last updated (ISO 8601 format).
    """


class Automation(TypedDict):
    """
    Automation represents a full automation object.

    Attributes:
        object (str): The object type, always "automation"
        id (str): The automation ID
        name (str): The automation name
        status (AutomationStatus): Current status
        created_at (str): Creation date/time
        updated_at (str): Last update date/time
        steps (List[AutomationResponseStep]): Steps in the active version
        connections (List[AutomationConnection]): Connections between steps
    """

    object: str
    """
    The object type, always "automation".
    """
    id: str
    """
    The automation ID.
    """
    name: str
    """
    The automation name.
    """
    status: AutomationStatus
    """
    Current status of the automation.
    """
    created_at: str
    """
    When the automation was created (ISO 8601 format).
    """
    updated_at: str
    """
    When the automation was last updated (ISO 8601 format).
    """
    steps: List[AutomationResponseStep]
    """
    Steps in the active version of the automation.
    """
    connections: List[AutomationConnection]
    """
    Connections between steps in the active version of the automation.
    """


class AutomationRunListItem(TypedDict):
    """
    AutomationRunListItem represents an automation run in list responses.

    Attributes:
        id (str): The run ID
        status (AutomationRunStatus): Current run status
        started_at (Union[str, None]): When the run started
        completed_at (Union[str, None]): When the run completed
        created_at (str): When the run was created
    """

    id: str
    """
    The run ID.
    """
    status: AutomationRunStatus
    """
    Current run status.
    """
    started_at: Union[str, None]
    """
    When the run started (ISO 8601 format), or None.
    """
    completed_at: Union[str, None]
    """
    When the run completed (ISO 8601 format), or None.
    """
    created_at: str
    """
    When the run was created (ISO 8601 format).
    """


class AutomationRun(TypedDict):
    """
    AutomationRun represents a full automation run object.

    Attributes:
        object (str): The object type, always "automation_run"
        id (str): The run ID
        status (AutomationRunStatus): Current run status
        started_at (Union[str, None]): When the run started
        completed_at (Union[str, None]): When the run completed
        created_at (str): When the run was created
        steps (List[AutomationRunStep]): Steps in the run, sorted in graph order
    """

    object: str
    """
    The object type, always "automation_run".
    """
    id: str
    """
    The run ID.
    """
    status: AutomationRunStatus
    """
    Current run status.
    """
    started_at: Union[str, None]
    """
    When the run started (ISO 8601 format), or None.
    """
    completed_at: Union[str, None]
    """
    When the run completed (ISO 8601 format), or None.
    """
    created_at: str
    """
    When the run was created (ISO 8601 format).
    """
    steps: List[AutomationRunStep]
    """
    Steps in the run, sorted in graph order.
    """
