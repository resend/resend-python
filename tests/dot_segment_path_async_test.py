import pytest

import resend
from tests.conftest import AsyncResendBaseTest

# flake8: noqa

pytestmark = pytest.mark.asyncio


class TestDotSegmentPathAsync(AsyncResendBaseTest):
    async def test_dot_segment_ids_are_rejected_before_sending_async(self) -> None:
        with pytest.raises(ValueError, match="cannot be `.` or `..`"):
            await resend.Domains.remove_async("../api-keys/key_id")
        self.mock.assert_not_called()
