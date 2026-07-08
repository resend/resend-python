import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestResendOAuthGrantsAsync(AsyncResendBaseTest):
    async def test_oauth_grants_list_async(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "650e8400-e29b-41d4-a716-446655440001",
                        "client_id": "430eed87-632a-4ea6-90db-0aace67ec228",
                        "scopes": ["emails:send"],
                        "created_at": "2023-06-21T06:10:36.144Z",
                        "revoked_at": None,
                        "revoked_reason": None,
                        "client": {
                            "name": "Resend CLI",
                            "logo_uri": "https://example.com/logo.png",
                        },
                    }
                ],
            }
        )

        grants: resend.OAuthGrants.ListResponse = await resend.OAuthGrants.list_async()
        for grant in grants["data"]:
            assert grant["id"] == "650e8400-e29b-41d4-a716-446655440001"
            assert grant["client_id"] == "430eed87-632a-4ea6-90db-0aace67ec228"
            assert grant["scopes"] == ["emails:send"]
            assert grant["client"]["name"] == "Resend CLI"

    async def test_list_oauth_grants_async_returns_no_content_error(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.OAuthGrants.list_async()

    async def test_oauth_grants_revoke_async(self) -> None:
        self.set_mock_json(
            {
                "object": "oauth_grant",
                "id": "650e8400-e29b-41d4-a716-446655440001",
                "revoked_at": "2023-06-22T06:10:36.144Z",
                "revoked_reason": "revoked_from_api",
            }
        )

        revoked: resend.OAuthGrants.RevokeOAuthGrantResponse = (
            await resend.OAuthGrants.revoke_async(
                oauth_grant_id="650e8400-e29b-41d4-a716-446655440001",
            )
        )
        assert revoked["object"] == "oauth_grant"
        assert revoked["id"] == "650e8400-e29b-41d4-a716-446655440001"
        assert revoked["revoked_at"] == "2023-06-22T06:10:36.144Z"
        assert revoked["revoked_reason"] == "revoked_from_api"

    async def test_revoke_oauth_grant_async_returns_no_content_error(
        self,
    ) -> None:
        self.set_mock_json(None)
        with pytest.raises(NoContentError):
            _ = await resend.OAuthGrants.revoke_async(oauth_grant_id="grant-1")
