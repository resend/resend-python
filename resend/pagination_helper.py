from typing import Any, Dict, Optional
from urllib.parse import urlencode


class PaginationHelper:
    """Helper class for building paginated URLs with query parameters."""

    @staticmethod
    def build_paginated_path(path: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Build a path with query parameters for pagination.

        Args:
            path: The base API path (e.g., "/api-keys")
            params: Optional dictionary of query parameters

        Returns:
            The path with query parameters appended if any valid params exist
        """
        if not params:
            return path

        # Filter out None values
        query_params = {k: v for k, v in params.items() if v is not None}

        if not query_params:
            return path

        # Build the query string
        query_string = urlencode(query_params)

        # Append to path with proper separator
        separator = "&" if "?" in path else "?"
        return f"{path}{separator}{query_string}"
