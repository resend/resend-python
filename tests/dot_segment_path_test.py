from typing import Any, Callable, List

import pytest

import resend
from resend._path import has_dot_segment
from tests.conftest import ResendBaseTest

# flake8: noqa

DOT_SEGMENT_CALLS: List[Callable[[], Any]] = [
    lambda: resend.Emails.get(".."),
    lambda: resend.Emails.cancel(".."),
    lambda: resend.Domains.remove("."),
    lambda: resend.Domains.remove("../api-keys/key_id"),
    lambda: resend.Domains.get("%2E%2E"),
]

DOT_SEGMENT_PATHS = [
    "/emails/..",
    "/emails/./cancel",
    "/domains/../api-keys/key_id",
    "/emails/%2E%2E/cancel",
    "/emails/%2e.",
    "/emails/.%2E?limit=1",
]

SAFE_PATHS = [
    "/emails/4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
    "/emails/...",
    "/emails/..%2Fapi-keys",
    "/contacts/john.doe@example.com",
    "/templates?after=..",
    "/emails/x#/..",
]


class TestDotSegmentPath(ResendBaseTest):
    def test_dot_segment_ids_are_rejected_before_sending(self) -> None:
        for call in DOT_SEGMENT_CALLS:
            with self.subTest(call=call):
                with pytest.raises(ValueError, match="cannot be `.` or `..`"):
                    call()
        self.mock.assert_not_called()

    def test_dotted_ids_are_still_sent(self) -> None:
        self.set_mock_json({})
        resend.Domains.get("example.com")
        resend.Contacts.get(email="john.doe@example.com")
        resend.Domains.get("...")
        urls = [c.kwargs["url"] for c in self.mock.call_args_list]
        assert urls[0].endswith("/domains/example.com")
        assert urls[1].endswith("/contacts/john.doe%40example.com")
        assert urls[2].endswith("/domains/...")

    def test_has_dot_segment(self) -> None:
        for path in DOT_SEGMENT_PATHS:
            with self.subTest(path=path):
                assert has_dot_segment(path)

    def test_has_no_dot_segment(self) -> None:
        for path in SAFE_PATHS:
            with self.subTest(path=path):
                assert not has_dot_segment(path)
