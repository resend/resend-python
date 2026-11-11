import json

import httpx
import pytest
import requests

import resend
from resend.http_client_httpx import HTTPXClient

RESPONSE = {"id": "email-1", "object": "list", "data": [], "has_more": False}
SEND_PARAMS = {
    "from": "sender@example.test",
    "to": ["recipient@example.test"],
    "subject": "Test",
    "text": "Test content",
}


@pytest.mark.parametrize("operation", ["get", "list", "list_page", "send"])
def test_sync_email_request_body(monkeypatch, operation):
    seen = []

    def send(session, request, **kwargs):
        seen.append(request)
        response = requests.Response()
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response._content = json.dumps(RESPONSE).encode()
        return response

    monkeypatch.setattr(requests.Session, "send", send)
    monkeypatch.setattr(resend, "api_key", "test-key")
    monkeypatch.setattr(resend, "default_http_client", resend.RequestsClient())

    if operation == "get":
        result = resend.Emails.get("email-1")
    elif operation == "list":
        result = resend.Emails.list()
    elif operation == "list_page":
        result = resend.Emails.list({"limit": 5, "after": "cursor-1"})
    else:
        result = resend.Emails.send(SEND_PARAMS)

    assert result["id"] == "email-1"
    request = seen[0]
    assert request.headers["Authorization"] == "Bearer test-key"
    if operation == "send":
        assert json.loads(request.body) == SEND_PARAMS
    else:
        assert request.body is None
        assert "Content-Type" not in request.headers
    if operation == "list_page":
        assert request.url.endswith("/emails?limit=5&after=cursor-1")


@pytest.mark.parametrize("operation", ["get", "list", "list_page", "send"])
async def test_async_email_request_body(monkeypatch, operation):
    seen = []

    def respond(request):
        seen.append(request)
        return httpx.Response(200, json=RESPONSE)

    original_client = httpx.AsyncClient

    def client_factory(**kwargs):
        return original_client(transport=httpx.MockTransport(respond), **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client_factory)
    monkeypatch.setattr(resend, "api_key", "test-key")
    monkeypatch.setattr(resend, "default_async_http_client", HTTPXClient())

    if operation == "get":
        result = await resend.Emails.get_async("email-1")
    elif operation == "list":
        result = await resend.Emails.list_async()
    elif operation == "list_page":
        result = await resend.Emails.list_async({"limit": 5, "after": "cursor-1"})
    else:
        result = await resend.Emails.send_async(SEND_PARAMS)

    assert result["id"] == "email-1"
    request = seen[0]
    assert request.headers["Authorization"] == "Bearer test-key"
    if operation == "send":
        assert json.loads(request.content) == SEND_PARAMS
    else:
        assert request.content == b""
        assert "Content-Type" not in request.headers
    if operation == "list_page":
        assert str(request.url).endswith("/emails?limit=5&after=cursor-1")
