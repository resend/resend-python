import unittest

from resend.response import ResponseDict


class TestResponseDict(unittest.TestCase):
    def test_response_dict_behaves_like_dict(self) -> None:
        """Test that ResponseDict acts exactly like a regular dict."""
        data = {"id": "123", "status": "sent"}
        response = ResponseDict(data, headers={"x-request-id": "abc"})

        # Dict access
        assert response["id"] == "123"
        assert response["status"] == "sent"
        assert response.get("id") == "123"
        assert response.get("missing", "default") == "default"

        # Dict methods
        assert list(response.keys()) == ["id", "status"]
        assert list(response.values()) == ["123", "sent"]
        assert len(response) == 2

        # Iteration
        keys = []
        for key in response:
            keys.append(key)
        assert keys == ["id", "status"]

        # Is instance of dict
        assert isinstance(response, dict)

    def test_response_dict_headers_access(self) -> None:
        """Test that headers can be accessed via .headers attribute."""
        data = {"id": "123"}
        headers = {
            "x-request-id": "req_abc",
            "x-ratelimit-limit": "100",
            "x-ratelimit-remaining": "95",
        }
        response = ResponseDict(data, headers=headers)

        assert response.headers["x-request-id"] == "req_abc"
        assert response.headers["x-ratelimit-limit"] == "100"
        assert response.headers.get("x-ratelimit-remaining") == "95"
        assert response.headers.get("missing") is None

    def test_response_dict_empty_headers(self) -> None:
        """Test ResponseDict with no headers."""
        data = {"id": "123"}
        response = ResponseDict(data)

        assert response.headers == {}
        assert response["id"] == "123"

    def test_response_dict_empty_data(self) -> None:
        """Test ResponseDict with empty data."""
        response = ResponseDict({}, headers={"x-test": "value"})

        assert len(response) == 0
        assert response.headers["x-test"] == "value"

    def test_response_dict_equality(self) -> None:
        """Test that ResponseDict compares equal to equivalent dicts."""
        data = {"id": "123", "status": "sent"}
        response = ResponseDict(data, headers={"x-test": "value"})

        assert response == data
        assert response == {"id": "123", "status": "sent"}

    def test_response_dict_repr(self) -> None:
        """Test string representation of ResponseDict."""
        data = {"id": "123"}
        headers = {"x-request-id": "abc"}
        response = ResponseDict(data, headers=headers)

        repr_str = repr(response)
        assert "ResponseDict" in repr_str
        assert "'id': '123'" in repr_str
        assert "x-request-id" in repr_str

    def test_response_dict_modification(self) -> None:
        """Test that ResponseDict can be modified like a regular dict."""
        response = ResponseDict({"id": "123"}, headers={"x-test": "value"})

        # Modify dict
        response["new_key"] = "new_value"
        assert response["new_key"] == "new_value"

        # Update dict
        response.update({"another": "field"})
        assert response["another"] == "field"

        # Headers remain intact
        assert response.headers["x-test"] == "value"
