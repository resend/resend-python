from typing import List

from resend.domains._record import Record


class Domain:
    id: str
    """
    The domain ID
    """
    name: str
    """
    The domain name
    """
    created_at: str
    """
    When domain was created
    """
    status: str
    """
    Status of the domain: not_started, etc..
    """
    region: str
    """
    The region where emails will be sent from. Possible values: us-east-1' | 'eu-west-1' | 'sa-east-1' | 'ap-northeast-1'
    """
    records: List[Record]
    """
    The list of domain records
    """
    deleted: bool
    """
    Wether the domain is deleted or not
    """

    def __init__(self, id, name, region, created_at, status, records, deleted=False):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.status = status
        self.region = region
        self.records = records
        self.deleted = deleted

    @staticmethod
    def new_from_request(val) -> "Domain":
        domain = Domain(
            id=val["id"] if "id" in val else None,
            name=val["name"] if "name" in val else None,
            region=val["region"] if "region" in val else None,
            created_at=val["created_at"] if "created_at" in val else None,
            status=val["status"] if "status" in val else None,
            records=[Record.new_from_request(record) for record in val["records"]]
            if "records" in val
            else None,
            deleted=val["deleted"] if "deleted" in val else None,
        )
        return domain
