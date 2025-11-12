"""Response wrapper that includes headers while maintaining backward compatibility."""

from typing import Any, Dict, Mapping, Optional


class ResponseDict(dict[str, Any]):
    """A dictionary subclass that also carries response headers as an attribute.

    This class maintains full backward compatibility with existing code that
    expects a plain dictionary, while also providing access to HTTP response
    headers through the .headers attribute.
    """

    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ):
        """Initialize ResponseDict with data and optional headers.

        Args:
            data: The response data dictionary
            headers: The HTTP response headers
        """
        super().__init__(data or {})
        self.headers: Dict[str, str] = dict(headers) if headers else {}

    def __repr__(self) -> str:
        """Return a string representation including headers info."""
        dict_repr = dict.__repr__(self)
        return f"ResponseDict({dict_repr}, headers={self.headers})"
