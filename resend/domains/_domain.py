from typing import List, Union

from typing_extensions import Literal, TypedDict

from resend.domains._record import Record

DomainObject = Literal["domain"]


class ShortDomain(TypedDict):
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
    region: Literal["us-east-1", "eu-west-1", "sa-east-1", "ap-northeast-1"]
    """
    The region where emails will be sent from. 
    Possible values: us-east-1' | 'eu-west-1' | 'sa-east-1' | 'ap-northeast-1'
    """


class Domain(ShortDomain):
    object: DomainObject
    """
    The object type
    """
    records: Union[List[Record], None]
    """
    The list of domain records
    """
