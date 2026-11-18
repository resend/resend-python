from typing_extensions import Literal, NotRequired, TypedDict

TopicVisibility = Literal["public", "private"]


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
    visibility: NotRequired[TopicVisibility]
    """
    The visibility of the topic on the unsubscribe page. Possible values: public or private.
    """
    created_at: str
    """
    The date and time the topic was created.
    """
