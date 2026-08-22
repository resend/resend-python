from typing_extensions import TypedDict


class ClickedLink(TypedDict):
    id: str
    """
    An opaque cursor for this row, used only for pagination.
    It does not identify any entity in Resend.
    """
    url: str
    """
    The URL that was clicked.
    """
    clicks: int
    """
    Total number of clicks on this URL.
    """
    unique_clicks: int
    """
    Number of unique clicks on this URL.
    """
