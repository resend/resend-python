from typing import Dict, Union

from typing_extensions import Literal, TypedDict

EventSchemaFieldType = Literal["string", "number", "boolean", "date"]
"""
EventSchemaFieldType is the type of a field in an event schema.
Supported types: "string", "number", "boolean", "date"
"""

EventSchema = Dict[str, EventSchemaFieldType]
"""
EventSchema is a flat key/type map defining the structure of an event payload.
Keys are field names, values are the field types.
"""


class EventListItem(TypedDict):
    """
    EventListItem represents an event in list responses.

    Attributes:
        id (str): The event ID (UUID)
        name (str): The event name
        schema (Union[EventSchema, None]): The event schema definition
        created_at (str): Creation date/time
        updated_at (Union[str, None]): Last update date/time
    """

    id: str
    """
    The event ID (UUID).
    """
    name: str
    """
    The event name.
    """
    schema: Union[EventSchema, None]
    """
    The event schema definition, or None if no schema is defined.
    """
    created_at: str
    """
    When the event was created (ISO 8601 format).
    """
    updated_at: Union[str, None]
    """
    When the event was last updated (ISO 8601 format), or None.
    """


class Event(TypedDict):
    """
    Event represents a full event object.

    Attributes:
        object (str): The object type, always "event"
        id (str): The event ID (UUID)
        name (str): The event name
        schema (Union[EventSchema, None]): The event schema definition
        created_at (str): Creation date/time
        updated_at (Union[str, None]): Last update date/time
    """

    object: str
    """
    The object type, always "event".
    """
    id: str
    """
    The event ID (UUID).
    """
    name: str
    """
    The event name.
    """
    schema: Union[EventSchema, None]
    """
    The event schema definition, or None if no schema is defined.
    """
    created_at: str
    """
    When the event was created (ISO 8601 format).
    """
    updated_at: Union[str, None]
    """
    When the event was last updated (ISO 8601 format), or None.
    """
