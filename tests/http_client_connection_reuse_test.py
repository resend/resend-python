import asyncio
import json
import socketserver
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler
from typing import Any, Iterator, List, Tuple

import resend
from resend.http_client_httpx import HTTPXClient
from resend.http_client_requests import RequestsClient


class _ThreadedServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


@contextmanager
def serve() -> Iterator[Tuple[str, List[int]]]:
    """Run a local HTTP server and record how many TCP connections it accepts.

    Yields the base URL and the connection log. One entry is appended per
    accepted connection, so reuse shows up as a shorter log than the number of
    requests made.
    """
    connections: List[int] = []
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def setup(self) -> None:
            # setup() runs once per accepted TCP connection, not per request.
            with lock:
                connections.append(1)
            super().setup()

        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", 0))
            sent = json.loads(self.rfile.read(length))

            # Echo the subject back so a response delivered to the wrong
            # caller is detectable.
            body = json.dumps({"id": sent["subject"]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    httpd = _ThreadedServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    try:
        yield f"http://127.0.0.1:{httpd.server_address[1]}", connections
    finally:
        httpd.shutdown()
        httpd.server_close()


SEND_PARAMS: resend.Emails.SendParams = {
    "from": "hello@example.com",
    "to": ["world@example.com"],
    "subject": "Hi!",
    "html": "<b>hi</b>",
}


class TestSyncConnectionReuse:
    def setup_method(self) -> None:
        self._original_client = resend.default_http_client
        self._original_url = resend.api_url
        resend.api_key = "re_test"

    def teardown_method(self) -> None:
        resend.default_http_client = self._original_client
        resend.api_url = self._original_url
        resend.api_key = None

    def test_reuses_a_single_connection(self) -> None:
        with serve() as (url, connections):
            resend.api_url = url
            client = RequestsClient()
            resend.default_http_client = client

            try:
                for _ in range(5):
                    resend.Emails.send(SEND_PARAMS)
            finally:
                client.close()

            assert len(connections) == 1

    def test_close_is_idempotent(self) -> None:
        client = RequestsClient()
        client.close()
        client.close()

    def test_shared_session_keeps_responses_separate_across_threads(self) -> None:
        """The session is shared, so each caller must still get its own response."""
        with serve() as (url, _connections):
            resend.api_url = url
            client = RequestsClient()
            resend.default_http_client = client

            def send(index: int) -> Tuple[int, str]:
                params: resend.Emails.SendParams = {
                    "from": "hello@example.com",
                    "to": ["world@example.com"],
                    "subject": f"msg-{index}",
                    "html": "<b>hi</b>",
                }
                return index, resend.Emails.send(params)["id"]

            try:
                with ThreadPoolExecutor(max_workers=8) as pool:
                    results = list(pool.map(send, range(40)))
            finally:
                client.close()

            assert all(sent_id == f"msg-{index}" for index, sent_id in results)

    def test_works_as_a_context_manager(self) -> None:
        with serve() as (url, connections):
            resend.api_url = url

            with RequestsClient() as client:
                resend.default_http_client = client
                for _ in range(3):
                    resend.Emails.send(SEND_PARAMS)

            assert len(connections) == 1


class TestAsyncConnectionReuse:
    def setup_method(self) -> None:
        self._original_client = resend.default_async_http_client
        self._original_url = resend.api_url
        resend.api_key = "re_test"

    def teardown_method(self) -> None:
        resend.default_async_http_client = self._original_client
        resend.api_url = self._original_url
        resend.api_key = None

    def test_reuses_a_single_connection(self) -> None:
        with serve() as (url, connections):
            resend.api_url = url
            client = HTTPXClient()
            resend.default_async_http_client = client

            async def send_many() -> None:
                try:
                    for _ in range(5):
                        await resend.Emails.send_async(SEND_PARAMS)
                finally:
                    await client.aclose()

            asyncio.run(send_many())

            assert len(connections) == 1

    def test_recreates_the_client_when_the_event_loop_changes(self) -> None:
        """A client cached from a closed loop must not be reused on a new one."""
        with serve() as (url, connections):
            resend.api_url = url
            client = HTTPXClient()
            resend.default_async_http_client = client

            async def send_one() -> None:
                await resend.Emails.send_async(SEND_PARAMS)

            # Two separate loops. The second must not fail on the dead pool.
            asyncio.run(send_one())
            asyncio.run(send_one())

            # One connection per loop, and no error raised.
            assert len(connections) == 2

    def test_aclose_allows_a_later_request(self) -> None:
        with serve() as (url, connections):
            resend.api_url = url
            client = HTTPXClient()
            resend.default_async_http_client = client

            async def send_close_send() -> None:
                await resend.Emails.send_async(SEND_PARAMS)
                await client.aclose()
                await resend.Emails.send_async(SEND_PARAMS)
                await client.aclose()

            asyncio.run(send_close_send())

            assert len(connections) == 2
