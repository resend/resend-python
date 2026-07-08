from typing import List, Optional

from typing_extensions import TypedDict


class OAuthGrantClient(TypedDict):
    name: str
    """
    The name of the OAuth client the grant was issued to
    """
    logo_uri: Optional[str]
    """
    The URL of the OAuth client's logo, or None if not set
    """


class OAuthGrant(TypedDict):
    id: str
    """
    The OAuth grant ID
    """
    client_id: str
    """
    The ID of the OAuth client the grant was issued to
    """
    scopes: List[str]
    """
    The scopes granted to the OAuth client
    """
    created_at: str
    """
    The date and time the grant was created
    """
    revoked_at: Optional[str]
    """
    The date and time the grant was revoked, or None if it is still active
    """
    revoked_reason: Optional[str]
    """
    The reason the grant was revoked, or None if it is still active
    """
    client: OAuthGrantClient
    """
    The OAuth client the grant was issued to
    """
