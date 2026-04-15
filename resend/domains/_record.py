from typing_extensions import NotRequired, TypedDict


class Record(TypedDict):
    record: str
    """
    The domain record type, ie: SPF, DKIM, Inbound, Tracking, TrackingCAA.
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
    priority: NotRequired[int]
    """
    The domain record priority.
    """
