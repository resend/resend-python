from typing import Optional

from typing_extensions import Literal, TypedDict

from resend._base_response import BaseResponse

DomainClaimStatus = Literal[
    "pending",
    "verified",
    "completed",
    "blocked",
    "expired",
    "superseded",
    "canceled",
    "failed",
]

DomainClaimBlockedReason = Literal[
    "grace_period",
    "recent_owner_activity",
    "pending_scheduled_emails",
]


class DomainClaimRecord(TypedDict):
    """
    DomainClaimRecord is the TXT record to add to your DNS to prove ownership of the claimed domain.

    Attributes:
        type (str): The DNS record type. Always 'TXT' for domain claims.
        name (str): The name of the DNS record (the domain being claimed).
        value (str): The value of the TXT record.
        ttl (str): The time to live for the record.
    """

    type: str
    name: str
    value: str
    ttl: str


class DomainClaim(BaseResponse):
    """
    DomainClaim represents a claim for a domain that another Resend account has already verified.

    Attributes:
        object (str): Always 'domain_claim'.
        id (str): The ID of the claim.
        name (str): The name of the domain being claimed.
        status (DomainClaimStatus): The status of the claim.
        domain_id (Optional[str]): The ID of the placeholder domain created for the claim.
        region (Optional[str]): The region where the claimed domain will send from.
        record (DomainClaimRecord): The TXT record to add to your DNS to prove ownership.
        blocked_reason (Optional[DomainClaimBlockedReason]): Why the claim is currently blocked, if applicable.
        failure_reason (Optional[str]): Why the claim failed, if applicable.
        created_at (str): The date and time the claim was created.
        expires_at (str): The date and time the claim expires if not verified.
    """

    object: str
    id: str
    name: str
    status: DomainClaimStatus
    domain_id: Optional[str]
    region: Optional[str]
    record: DomainClaimRecord
    blocked_reason: Optional[DomainClaimBlockedReason]
    failure_reason: Optional[str]
    created_at: str
    expires_at: str
