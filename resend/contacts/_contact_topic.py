from typing_extensions import TypedDict


class ContactTopic(TypedDict):
    """
    ContactTopic represents a topic subscription for a contact.

    Attributes:
        id (str): The unique identifier for the topic
        name (str): The name of the topic
        description (str): The description of the topic
        subscription (str): The subscription status. Must be either "opt_in" or "opt_out"
    """

    id: str
    """
    The unique identifier for the topic.
    """
    name: str
    """
    The name of the topic.
    """
    description: str
    """
    The description of the topic.
    """
    subscription: str
    """
    The subscription status. Must be either "opt_in" or "opt_out".
    """


class TopicSubscriptionUpdate(TypedDict):
    """
    TopicSubscriptionUpdate represents an update to a topic subscription.

    Attributes:
        id (str): The topic ID
        subscription (str): The subscription action. Must be either "opt_in" or "opt_out"
    """

    id: str
    """
    The topic ID.
    """
    subscription: str
    """
    The subscription action. Must be either "opt_in" or "opt_out".
    """
