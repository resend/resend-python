from typing import Any, Callable, cast
from unittest.mock import AsyncMock, create_autospec

import pytest

import resend
from resend._path import has_dot_segment
from resend.http_client import HTTPClient
from resend.http_client_async import AsyncHTTPClient

# flake8: noqa

DOT_SEGMENT_CALLS = [
    lambda: resend.Emails.get(".."),
    lambda: resend.Emails.cancel(".."),
    lambda: resend.Domains.remove("."),
    lambda: resend.Domains.remove("../api-keys/key_id"),
    lambda: resend.Domains.get("%2E%2E"),
]


@pytest.fixture
def mock_client() -> Any:
    resend.api_key = "re_test"
    previous = resend.default_http_client
    client = create_autospec(HTTPClient, instance=True)
    client.request.return_value = (b"{}", 200, {"Content-Type": "application/json"})
    resend.default_http_client = client
    yield client
    resend.default_http_client = previous


@pytest.mark.parametrize("call", DOT_SEGMENT_CALLS)
def test_dot_segment_ids_are_rejected_before_sending(
    mock_client: Any, call: Callable[[], Any]
) -> None:
    with pytest.raises(ValueError, match="cannot be `.` or `..`"):
        call()
    mock_client.request.assert_not_called()


def test_dotted_ids_are_still_sent(mock_client: Any) -> None:
    resend.Domains.get("example.com")
    resend.Contacts.get(email="john.doe@example.com")
    resend.Domains.get("...")
    urls = [c.kwargs["url"] for c in mock_client.request.call_args_list]
    assert urls[0].endswith("/domains/example.com")
    assert urls[1].endswith("/contacts/john.doe%40example.com")
    assert urls[2].endswith("/domains/...")


@pytest.mark.asyncio
async def test_dot_segment_ids_are_rejected_before_sending_async() -> None:
    resend.api_key = "re_test"
    previous = resend.default_async_http_client
    client = create_autospec(AsyncHTTPClient, instance=True)
    client.request = AsyncMock(
        return_value=(b"{}", 200, {"Content-Type": "application/json"})
    )
    resend.default_async_http_client = cast(AsyncHTTPClient, client)
    try:
        with pytest.raises(ValueError, match="cannot be `.` or `..`"):
            await resend.Domains.remove_async("../api-keys/key_id")
        client.request.assert_not_called()
    finally:
        resend.default_async_http_client = previous


@pytest.mark.parametrize(
    "path",
    [
        "/emails/..",
        "/emails/./cancel",
        "/domains/../api-keys/key_id",
        "/emails/%2E%2E/cancel",
        "/emails/%2e.",
        "/emails/.%2E?limit=1",
    ],
)
def test_has_dot_segment(path: str) -> None:
    assert has_dot_segment(path)


@pytest.mark.parametrize(
    "path",
    [
        "/emails/4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
        "/emails/...",
        "/emails/..%2Fapi-keys",
        "/contacts/john.doe@example.com",
        "/templates?after=..",
        "/emails/x#/..",
    ],
)
def test_has_no_dot_segment(path: str) -> None:
    assert not has_dot_segment(path)
