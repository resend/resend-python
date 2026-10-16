from typing import Any, Dict, Mapping, Optional
from urllib.parse import quote

from resend.pagination_helper import PaginationHelper


def build_inbox_query_path(path: str, params: Optional[Mapping[str, Any]] = None) -> str:
    """
    Build a path with the query parameters of an inbox list or search call.
    Lists become comma-separated values, and empty lists are left out.
    Booleans become the literal ``true`` or ``false`` that the API accepts.

    Args:
        path: The base API path (e.g., "/inboxes/{inbox_id}/threads")
        params: Optional query parameters

    Returns:
        The path with the query parameters appended, if any are set
    """
    if not params:
        return path

    query: Dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            query[key] = "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            if value:
                query[key] = ",".join(str(item) for item in value)
        else:
            query[key] = value

    return PaginationHelper.build_paginated_path(path, query)


def without_keys(params: Mapping[str, Any], *keys: str) -> Dict[str, Any]:
    """
    Return a copy of the params without the given keys. The SDK puts the
    path IDs in the params dict, but the API takes them in the path only.
    """
    return {k: v for k, v in params.items() if k not in keys}


def inbox_path(inbox_id: str) -> str:
    """
    Return the path of an inbox. The API takes the Inbox ID or the inbox email
    address, and an address must be percent-encoded to fit in the path.
    """
    return f"/inboxes/{quote(inbox_id, safe='')}"
