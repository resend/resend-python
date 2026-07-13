import resend
from resend.exceptions import NoContentError
from tests.conftest import ResendBaseTest

# flake8: noqa


class TestResendOAuthGrants(ResendBaseTest):
    def test_oauth_grants_list(self) -> None:
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

        grants: resend.OAuthGrants.ListResponse = resend.OAuthGrants.list()
        assert grants["object"] == "list"
        assert grants["has_more"] is False
        for grant in grants["data"]:
            assert grant["id"] == "650e8400-e29b-41d4-a716-446655440001"
            assert grant["client_id"] == "430eed87-632a-4ea6-90db-0aace67ec228"
            assert grant["scopes"] == ["emails:send"]
            assert grant["created_at"] == "2023-06-21T06:10:36.144Z"
            assert grant["revoked_at"] is None
            assert grant["revoked_reason"] is None
            assert grant["client"]["name"] == "Resend CLI"
            assert grant["client"]["logo_uri"] == "https://example.com/logo.png"

    def test_oauth_grants_list_revoked_grant(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "650e8400-e29b-41d4-a716-446655440002",
                        "client_id": "430eed87-632a-4ea6-90db-0aace67ec228",
                        "scopes": ["emails:send", "domains:read"],
                        "created_at": "2023-06-20T06:10:36.144Z",
                        "revoked_at": "2023-06-22T06:10:36.144Z",
                        "revoked_reason": "revoked_from_api",
                        "client": {
                            "name": "Resend CLI",
                            "logo_uri": None,
                        },
                    }
                ],
            }
        )

        grants: resend.OAuthGrants.ListResponse = resend.OAuthGrants.list()
        grant = grants["data"][0]
        assert grant["revoked_at"] == "2023-06-22T06:10:36.144Z"
        assert grant["revoked_reason"] == "revoked_from_api"
        assert grant["client"]["logo_uri"] is None

    def test_list_oauth_grants_returns_no_content_error(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.OAuthGrants.list()

    def test_oauth_grants_list_with_pagination_params(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": True,
                "data": [
                    {
                        "id": "grant-1",
                        "client_id": "client-1",
                        "scopes": ["emails:send"],
                        "created_at": "2023-06-21T06:10:36.144Z",
                        "revoked_at": None,
                        "revoked_reason": None,
                        "client": {"name": "Resend CLI", "logo_uri": None},
                    },
                    {
                        "id": "grant-2",
                        "client_id": "client-1",
                        "scopes": ["emails:send"],
                        "created_at": "2023-06-20T06:10:36.144Z",
                        "revoked_at": None,
                        "revoked_reason": None,
                        "client": {"name": "Resend CLI", "logo_uri": None},
                    },
                ],
            }
        )

        params: resend.OAuthGrants.ListParams = {
            "limit": 10,
            "after": "previous-grant-id",
        }
        grants: resend.OAuthGrants.ListResponse = resend.OAuthGrants.list(params=params)
        assert grants["object"] == "list"
        assert grants["has_more"] is True
        assert len(grants["data"]) == 2
        assert grants["data"][0]["id"] == "grant-1"
        assert grants["data"][1]["id"] == "grant-2"

    def test_oauth_grants_list_with_before_param(self) -> None:
        self.set_mock_json(
            {
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "grant-3",
                        "client_id": "client-1",
                        "scopes": ["emails:send"],
                        "created_at": "2023-06-19T06:10:36.144Z",
                        "revoked_at": None,
                        "revoked_reason": None,
                        "client": {"name": "Resend CLI", "logo_uri": None},
                    }
                ],
            }
        )

        params: resend.OAuthGrants.ListParams = {"limit": 5, "before": "later-grant-id"}
        grants: resend.OAuthGrants.ListResponse = resend.OAuthGrants.list(params=params)
        assert grants["object"] == "list"
        assert grants["has_more"] is False
        assert len(grants["data"]) == 1
        assert grants["data"][0]["id"] == "grant-3"

    def test_oauth_grants_revoke(self) -> None:
        self.set_mock_json(
            {
                "object": "oauth_grant",
                "id": "650e8400-e29b-41d4-a716-446655440001",
                "revoked_at": "2023-06-22T06:10:36.144Z",
                "revoked_reason": "revoked_from_api",
            }
        )

        revoked: resend.OAuthGrants.RevokeOAuthGrantResponse = (
            resend.OAuthGrants.revoke(
                oauth_grant_id="650e8400-e29b-41d4-a716-446655440001",
            )
        )
        assert revoked["object"] == "oauth_grant"
        assert revoked["id"] == "650e8400-e29b-41d4-a716-446655440001"
        assert revoked["revoked_at"] == "2023-06-22T06:10:36.144Z"
        assert revoked["revoked_reason"] == "revoked_from_api"

    def test_revoke_oauth_grant_returns_no_content_error(self) -> None:
        self.set_mock_json(None)
        with self.assertRaises(NoContentError):
            _ = resend.OAuthGrants.revoke(oauth_grant_id="grant-1")
