import json
from typing import Any, List, Mapping, Tuple

import httpx
import pytest

import resend
from resend.exceptions import ResendError
from resend.http_client_async import AsyncHTTPClient

pytestmark = pytest.mark.asyncio

AUTOMATIC_CLIENT = resend.default_async_http_client


class NamedHTTPXClient(resend.HTTPXClient):
    def __init__(self, name: str, timeout: int = 60) -> None:
        super().__init__(timeout=timeout)
        self.name = name

    async def request(
        self, *args: Any, **kwargs: Any
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        kwargs["headers"] = {**kwargs["headers"], "x-test-client": self.name}
        return await super().request(*args, **kwargs)


class FailingAsyncClient(AsyncHTTPClient):
    async def request(
        self, *args: Any, **kwargs: Any
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        raise RuntimeError("custom transport failed")


@pytest.fixture  # type: ignore
def network(monkeypatch: pytest.MonkeyPatch) -> List[httpx.Request]:
    requests: List[httpx.Request] = []
    real_async_client = httpx.AsyncClient

    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        body: Any = {"id": request.headers.get("x-test-client", "automatic")}
        if request.url.path == "/usage":
            body = {
                "object": "usage",
                "emails": {
                    "daily": {
                        "used": 0,
                        "limit": 100,
                        "sent": 0,
                        "received": 0,
                        "resets_at": "2026-01-02T00:00:00Z",
                    },
                    "monthly": {
                        "used": 0,
                        "limit": 1000,
                        "sent": 0,
                        "received": 0,
                        "resets_at": "2026-02-01T00:00:00Z",
                    },
                },
                "contacts": {"used": 0, "limit": 1000},
                "segments": {"used": 0, "limit": 3},
                "broadcasts": {"used": 0, "limit": None},
                "ai_credits": {
                    "used": 0,
                    "limit": 100,
                    "next_increase_at": "2026-01-02T00:00:00Z",
                },
                "automation_runs": {
                    "used": 0,
                    "limit": 100,
                    "resets_at": "2026-02-01T00:00:00Z",
                },
                "domains": {"used": 1, "limit": 10},
                "rate_limit": {"limit": 10, "duration": "1000ms"},
            }
        elif request.method == "GET":
            body.update(
                {
                    "object": "email",
                    "message_id": "<test@example.com>",
                    "from": "team@example.com",
                    "to": ["user@example.com"],
                    "created_at": "2026-01-01T00:00:00Z",
                    "subject": "Test",
                    "html": "",
                    "text": "Hello",
                    "bcc": [],
                    "cc": [],
                    "reply_to": [],
                    "last_event": "delivered",
                }
            )
        return httpx.Response(
            200,
            json=body,
            headers={"x-request-id": "req_test"},
        )

    def isolated_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        kwargs["transport"] = httpx.MockTransport(respond)
        return real_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", isolated_client)
    monkeypatch.setattr(resend, "api_key", "re_test")
    monkeypatch.setattr(resend, "api_url", "https://test.invalid")
    monkeypatch.setattr(resend, "default_http_client", resend.RequestsClient())
    monkeypatch.setattr(resend, "default_async_http_client", AUTOMATIC_CLIENT)
    return requests


@pytest.mark.parametrize("resource", ["send", "get", "usage"])  # type: ignore
async def test_legacy_async_client_overrides_automatic_client(
    monkeypatch: pytest.MonkeyPatch, network: List[httpx.Request], resource: str
) -> None:
    monkeypatch.setattr(resend, "default_http_client", NamedHTTPXClient("legacy"))

    response: Any
    if resource == "send":
        response = await resend.Emails.send_async(
            {
                "from": "team@example.com",
                "to": ["user@example.com"],
                "subject": "Test",
                "text": "Hello",
            },
            {"idempotency_key": "test-send"},
        )
        assert network[0].method == "POST"
        assert json.loads(network[0].content)["subject"] == "Test"
        assert network[0].headers["idempotency-key"] == "test-send"
    elif resource == "get":
        response = await resend.Emails.get_async("email_1")
        assert network[0].url.path == "/emails/email_1"
    else:
        response = await resend.Usage.get_async()
        assert network[0].url.path == "/usage"
        assert response["object"] == "usage"

    assert network[0].headers.get("x-test-client") == "legacy"
    assert response["http_headers"]["x-request-id"] == "req_test"
    assert len(network) == 1
    assert network[0].headers["authorization"] == "Bearer re_test"
    assert network[0].extensions["timeout"]["read"] == 60


async def test_legacy_httpx_client_uses_configured_timeout(
    monkeypatch: pytest.MonkeyPatch, network: List[httpx.Request]
) -> None:
    monkeypatch.setattr(resend, "default_http_client", resend.HTTPXClient(timeout=45))

    await resend.Emails.get_async("email_1")

    assert network[0].extensions["timeout"]["read"] == 45


async def test_explicit_dedicated_client_has_priority_over_legacy_client(
    monkeypatch: pytest.MonkeyPatch, network: List[httpx.Request]
) -> None:
    monkeypatch.setattr(resend, "default_http_client", NamedHTTPXClient("legacy"))
    monkeypatch.setattr(
        resend, "default_async_http_client", NamedHTTPXClient("dedicated", timeout=90)
    )

    response = await resend.Emails.get_async("email_1")

    assert response["id"] == "dedicated"
    assert network[0].extensions["timeout"]["read"] == 90


async def test_explicit_httpx_client_has_priority_over_legacy_client(
    monkeypatch: pytest.MonkeyPatch, network: List[httpx.Request]
) -> None:
    monkeypatch.setattr(resend, "default_http_client", NamedHTTPXClient("legacy"))
    monkeypatch.setattr(
        resend, "default_async_http_client", resend.HTTPXClient(timeout=75)
    )

    response = await resend.Emails.get_async("email_1")

    assert response["id"] == "automatic"
    assert network[0].extensions["timeout"]["read"] == 75


async def test_automatic_client_is_used_with_sync_default(
    network: List[httpx.Request],
) -> None:
    response = await resend.Emails.get_async("email_1")

    assert response["id"] == "automatic"
    assert network[0].extensions["timeout"]["read"] == 30
    assert isinstance(resend.default_http_client, resend.RequestsClient)


async def test_legacy_client_is_used_when_dedicated_client_is_none(
    monkeypatch: pytest.MonkeyPatch, network: List[httpx.Request]
) -> None:
    monkeypatch.setattr(resend, "default_http_client", NamedHTTPXClient("legacy"))
    monkeypatch.setattr(resend, "default_async_http_client", None)

    response = await resend.Emails.get_async("email_1")

    assert response["id"] == "legacy"
    assert network[0].extensions["timeout"]["read"] == 60


async def test_restoring_automatic_client_restores_legacy_priority(
    monkeypatch: pytest.MonkeyPatch, network: List[httpx.Request]
) -> None:
    monkeypatch.setattr(resend, "default_http_client", NamedHTTPXClient("legacy"))
    monkeypatch.setattr(
        resend, "default_async_http_client", NamedHTTPXClient("dedicated")
    )
    assert (await resend.Emails.get_async("email_1"))["id"] == "dedicated"

    monkeypatch.setattr(resend, "default_async_http_client", AUTOMATIC_CLIENT)

    assert (await resend.Emails.get_async("email_1"))["id"] == "legacy"
    assert len(network) == 2


async def test_missing_async_client_retains_configuration_error(
    monkeypatch: pytest.MonkeyPatch, network: List[httpx.Request]
) -> None:
    monkeypatch.setattr(resend, "default_async_http_client", None)

    with pytest.raises(ResendError) as error:
        await resend.Emails.get_async("email_1")

    assert error.value.error_type == "AsyncClientNotConfigured"
    assert error.value.code == 500
    assert network == []


@pytest.mark.parametrize("dedicated", [False, True])  # type: ignore
async def test_selected_custom_client_error_is_not_bypassed(
    monkeypatch: pytest.MonkeyPatch,
    network: List[httpx.Request],
    dedicated: bool,
) -> None:
    if dedicated:
        monkeypatch.setattr(resend, "default_http_client", NamedHTTPXClient("legacy"))
        monkeypatch.setattr(resend, "default_async_http_client", FailingAsyncClient())
    else:
        monkeypatch.setattr(resend, "default_http_client", FailingAsyncClient())

    with pytest.raises(ResendError) as error:
        await resend.Emails.get_async("email_1")

    assert error.value.error_type == "HttpClientError"
    assert "custom transport failed" in str(error.value)
    assert network == []
