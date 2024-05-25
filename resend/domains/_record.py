from typing_extensions import TypedDict


class Record(TypedDict):
    record: str
    """
    The domain record type, ie: SPF.
    """
    name: str
    """
    The domain record name.
    """
    type: str
    """
    The domain record type, ie: MX.
    """
    ttl: str
    """
    The domain record time to live.
    """
    status: str
    """
    The domain record status: not_started, etc..
    """
    value: str
    """
    The domain record value.
    """
    priority: int
    """
    The domain record priority.
    """
