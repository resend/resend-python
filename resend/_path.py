import re

_DOT_SEGMENT = re.compile(r"^(?:\.|%2e){1,2}$", re.IGNORECASE)


def has_dot_segment(path: str) -> bool:
    """Whether a request path contains a `.` or `..` segment.

    HTTP clients resolve these before sending (requests/urllib3 and httpx both
    do), so an id such as "../api-keys/key_id" would reach another endpoint.
    """
    pathname = re.split(r"[?#]", path, maxsplit=1)[0]
    return any(_DOT_SEGMENT.match(segment) for segment in pathname.split("/"))


def ensure_no_dot_segments(path: str) -> None:
    if has_dot_segment(path):
        raise ValueError("Path parameters cannot be `.` or `..`.")
