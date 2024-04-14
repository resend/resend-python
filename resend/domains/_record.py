class Record:
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

    def __init__(
            self, record, name, type, ttl,
            status, value, priority):
        self.record = record
        self.name = name
        self.type = type
        self.ttl = ttl
        self.status = status
        self.value = value
        self.priority = priority

    @staticmethod
    def new_from_request(val) -> "Record":
        return Record(
            record=val["record"] if "record" in val else None,
            name=val["name"] if "name" in val else None,
            type=val["type"] if "type" in val else None,
            ttl=val["ttl"] if "ttl" in val else None,
            status=val["status"] if "status" in val else None,
            value=val["value"] if "value" in val else None,
            priority=val["priority"] if "priority" in val else None,
        )