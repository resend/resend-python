import pytest

import resend
from resend.exceptions import NoContentError
from tests.conftest import AsyncResendBaseTest
from tests.domain_forge_test import forge_domain_json

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestDomainForgeAsync(AsyncResendBaseTest):
    async def test_domain_forge_enable_async(self) -> None:
        self.set_mock_json(forge_domain_json())

        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
            "return_path": "send",
        }
        domain = await resend.Domains.Forge.enable_async(params)
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["name"] == "example.com"

    async def test_domain_forge_enable_async_without_return_path(self) -> None:
        self.set_mock_json(forge_domain_json())

        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
        }
        domain = await resend.Domains.Forge.enable_async(params)
        assert domain["id"] == "d91cd9bd-1176-453e-8fc1-35364d380206"
        assert domain["status"] == "pending"

    async def test_should_enable_forge_async_raise_exception_when_no_content(
        self,
    ) -> None:
        self.set_mock_json(None)
        params: resend.Domains.Forge.EnableParams = {
            "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
        }
        with pytest.raises(NoContentError):
            _ = await resend.Domains.Forge.enable_async(params)
