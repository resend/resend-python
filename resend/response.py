from typing import Any, Dict


class ResponseDict(Dict[str, Any]):
    """Dict subclass that supports attribute-style access.

    This allows SDK responses to be accessed using either dict syntax
    (response['data']) or attribute syntax (response.data), providing
    consistency with other Resend SDKs (e.g., Node.js).
    """

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )
