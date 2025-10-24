from typing_extensions import TypedDict


class Topic(TypedDict):
    id: str
    """
    The unique identifier of the topic.
    """
    name: str
    """
    The topic name.
    """
    default_subscription: str
    """
    The default subscription preference for new contacts. Possible values: opt_in or opt_out.
    """
    description: str
    """
    The topic description.
    """
    created_at: str
    """
    The date and time the topic was created.
    """
