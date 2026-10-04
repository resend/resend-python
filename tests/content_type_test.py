import asyncio
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest

from resend.async_request import AsyncRequest
from resend.exceptions import RateLimitError, ResendError
from resend.request import Request


def _perform_request(
    use_async: bool, content: bytes, status_code: int, headers: Dict[str, str]
) -> Dict[str, Any]:
    if use_async:
        async_client = AsyncMock()
        async_client.request.return_value = (content, status_code, headers)
        with patch("resend.default_async_http_client", async_client):
            req = AsyncRequest[Dict[str, Any]]("/emails", {}, "get")
            return asyncio.run(req.perform_with_content())

    sync_client = Mock()
    sync_client.request.return_value = (content, status_code, headers)
    with patch("resend.default_http_client", sync_client):
        return Request[Dict[str, Any]]("/emails", {}, "get").perform_with_content()


@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("header_name", ["content-type", "Content-Type"])
@pytest.mark.parametrize(
    "content_type",
    [
        "application/json",
        "application/json; charset=utf-8",
        "Application/JSON",
        "APPLICATION/JSON; CHARSET=UTF-8",
        " application/json ; charset=utf-8 ",
    ],
)
class TestJsonContentType:
    def test_json_content_type_is_accepted(
        self, use_async: bool, header_name: str, content_type: str
    ) -> None:
        headers = {header_name: content_type}
        response = _perform_request(use_async, b'{"id":"email_123"}', 200, headers)

        assert response["id"] == "email_123"
        assert response["http_headers"] == headers

    def test_json_error_preserves_error_type_and_headers(
        self, use_async: bool, header_name: str, content_type: str
    ) -> None:
        headers = {header_name: content_type, "retry-after": "2"}
        content = b'{"name":"rate_limit_exceeded","message":"Too many requests"}'

        with pytest.raises(RateLimitError) as error:
            _perform_request(use_async, content, 429, headers)

        assert error.value.code == 429
        assert error.value.error_type == "rate_limit_exceeded"
        assert error.value.message == "Too many requests"
        assert error.value.headers == headers


@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize(
    "content_type",
    ["text/plain", "application/jsonp", "text/plain; note=application/json", ""],
)
@pytest.mark.parametrize("status_code", [200, 429])
class TestNonJsonContentType:
    def test_non_json_content_type_is_rejected(
        self, use_async: bool, content_type: str, status_code: int
    ) -> None:
        headers = {"content-type": content_type, "retry-after": "2"}

        with pytest.raises(ResendError) as error:
            _perform_request(use_async, b'{"id":"email_123"}', status_code, headers)

        assert error.value.code == (status_code if status_code >= 400 else 500)
        assert error.value.headers == headers
        assert error.value.message == f"Expected JSON response but got: {content_type}"
