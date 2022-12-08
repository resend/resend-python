"""Klotty Exceptions module.

This module defines the base types for platform-wide error
codes as outlined in https://klotty.com/docs/errors.
"""


class KlottyError(Exception):
    """Base class for all errors raised by Klotty SDK.
    This is the parent class of all exceptions (server side)
    raised by the Klotty SDK. Developers can simply catch
    this class and inspect its `code` to implement more specific
    error handling. Note that for some client-side errors ie:
    some method argument missing, a ValueError would be raised.

    Args:
        code: A string error indicating the HTTP status code
        attributed to that Error.
        message: A human-readable error message string.
        suggested_action: A suggested action path to help the user.
    """

    def __init__(self, code: str, message: str, suggested_action: str = None):
        Exception.__init__(self, message)
        self.code = code
        self.suggested_action = suggested_action

    @property
    def code(self):
        return self.code

    @property
    def suggested_action(self):
        return self.suggested_action


class MissingApiKeyError:
    """see https://klotty.com/docs/errors"""

    def __init__(
        self,
    ):
        suggested_action = """Check the error message
        to see the list of missing fields."""
        KlottyError.__init__(
            self,
            message="The request body is missing one or more required fields.",
            suggested_action=suggested_action,
        )
