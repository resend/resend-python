import unittest

from resend.pagination_helper import PaginationHelper


class TestPaginationHelper(unittest.TestCase):
    def test_build_paginated_path_with_no_params(self) -> None:
        """Test that path is returned unchanged when no params are provided."""
        path = "/api-keys"
        result = PaginationHelper.build_paginated_path(path)
        assert result == "/api-keys"

    def test_build_paginated_path_with_none_params(self) -> None:
        """Test that path is returned unchanged when params is None."""
        path = "/api-keys"
        result = PaginationHelper.build_paginated_path(path, None)
        assert result == "/api-keys"

    def test_build_paginated_path_with_empty_params(self) -> None:
        """Test that path is returned unchanged when params dict is empty."""
        path = "/api-keys"
        result = PaginationHelper.build_paginated_path(path, {})
        assert result == "/api-keys"

    def test_build_paginated_path_with_single_param(self) -> None:
        """Test building path with a single query parameter."""
        path = "/api-keys"
        params = {"limit": 10}
        result = PaginationHelper.build_paginated_path(path, params)
        assert result == "/api-keys?limit=10"

    def test_build_paginated_path_with_multiple_params(self) -> None:
        """Test building path with multiple query parameters."""
        path = "/api-keys"
        params = {"limit": 10, "after": "key-123"}
        result = PaginationHelper.build_paginated_path(path, params)
        # Check both possible orderings since dict ordering may vary
        assert result in [
            "/api-keys?limit=10&after=key-123",
            "/api-keys?after=key-123&limit=10",
        ]

    def test_build_paginated_path_filters_none_values(self) -> None:
        """Test that None values are filtered out from params."""
        path = "/api-keys"
        params = {"limit": 10, "after": None, "before": "key-456"}
        result = PaginationHelper.build_paginated_path(path, params)
        # Should not include 'after' since it's None
        assert "after" not in result
        assert "limit=10" in result
        assert "before=key-456" in result

    def test_build_paginated_path_with_all_none_values(self) -> None:
        """Test that path is unchanged when all param values are None."""
        path = "/api-keys"
        params = {"limit": None, "after": None, "before": None}
        result = PaginationHelper.build_paginated_path(path, params)
        assert result == "/api-keys"

    def test_build_paginated_path_with_existing_query_string(self) -> None:
        """Test appending params to a path that already has a query string."""
        path = "/api-keys?status=active"
        params = {"limit": 5}
        result = PaginationHelper.build_paginated_path(path, params)
        assert result == "/api-keys?status=active&limit=5"

    def test_build_paginated_path_with_special_characters(self) -> None:
        """Test that special characters in params are properly URL encoded."""
        path = "/api-keys"
        params = {"after": "key with spaces", "tag": "test&value"}
        result = PaginationHelper.build_paginated_path(path, params)
        # Check URL encoding
        assert "key+with+spaces" in result or "key%20with%20spaces" in result
        assert "test%26value" in result

    def test_build_paginated_path_with_integer_values(self) -> None:
        """Test that integer values are properly converted to strings."""
        path = "/audiences"
        params = {"limit": 100, "offset": 0}
        result = PaginationHelper.build_paginated_path(path, params)
        assert "limit=100" in result
        assert "offset=0" in result
