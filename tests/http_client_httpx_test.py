from typing import Any, List

import httpx
import pytest

import resend
from resend.exceptions import ResendError

pytestmark = pytest.mark.asyncio

PARAMS: resend.Emails.SendParams = {
    "from": "team@example.com",
    "to": ["user@example.com"],
    "subject": "Test",
    "text": "Hello",
}


@pytest.fixture(autouse=True)  # type: ignore
def configure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(resend, "api_key", "re_test")
    monkeypatch.setattr(resend, "api_url", "https://test.invalid")
    monkeypatch.setattr(
        resend, "default_async_http_client", resend.default_async_http_client
    )


def recording_transport(requests: List[httpx.Request]) -> httpx.MockTransport:
    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"id": "email_1"})

    return httpx.MockTransport(respond)


async def test_provided_client_is_reused_and_left_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: List[httpx.Request] = []
    client = httpx.AsyncClient(transport=recording_transport(requests))

    def no_new_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        raise AssertionError("HTTPXClient created its own httpx.AsyncClient")

    monkeypatch.setattr(httpx, "AsyncClient", no_new_client)
    resend.default_async_http_client = resend.HTTPXClient(client=client)

    for _ in range(3):
        email = await resend.Emails.send_async(PARAMS)
        assert email["id"] == "email_1"

    assert len(requests) == 3
    assert all(r.url == "https://test.invalid/emails" for r in requests)
    assert not client.is_closed
    await client.aclose()


async def test_provided_client_sends_files() -> None:
    requests: List[httpx.Request] = []
    async with httpx.AsyncClient(transport=recording_transport(requests)) as client:
        content, status_code, _ = await resend.HTTPXClient(client=client).request(
            method="post",
            url="https://test.invalid/upload",
            headers={},
            files={"file": ("a.csv", b"email\n", "text/csv")},
            data={"name": "a"},
        )

    assert status_code == 200
    assert b"email_1" in content
    assert requests[0].headers["content-type"].startswith("multipart/form-data")
    assert b'name="name"' in requests[0].content


async def test_provided_client_request_error_raises_resend_error() -> None:
    def fail(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(fail)) as client:
        resend.default_async_http_client = resend.HTTPXClient(client=client)

        with pytest.raises(ResendError) as error:
            await resend.Emails.send_async(PARAMS)

    assert error.value.error_type == "HttpClientError"
    assert "connection refused" in error.value.message


async def test_without_client_a_new_client_is_created_per_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: List[httpx.Request] = []
    created: List[Any] = []
    real_async_client = httpx.AsyncClient

    def counting_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        created.append(kwargs.get("timeout"))
        kwargs["transport"] = recording_transport(requests)
        return real_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", counting_client)
    resend.default_async_http_client = resend.HTTPXClient(timeout=60)

    await resend.Emails.send_async(PARAMS)
    await resend.Emails.send_async(PARAMS)

    assert created == [60, 60]
    assert len(requests) == 2
