from typing import List, Union

from typing_extensions import NotRequired, TypedDict

from resend.domains._record import Record


class Domain(TypedDict):
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
    records: Union[List[Record], None]
    """
    The list of domain records
    """
    deleted: bool
    """
    Wether the domain is deleted or not
    """
    open_tracking: NotRequired[bool]
    """
    Track the open rate of each email.
    """
    click_tracking: NotRequired[bool]
    """
    Track clicks within the body of each HTML email.
    """
    tracking_subdomain: NotRequired[str]
    """
    The custom subdomain used for click and open tracking links (e.g., "links").
    """
