"""Klotty Exceptions module.

This module defines the base types for platform-wide error
codes as outlined in https://klotty.com/docs/errors.
"""


from typing import Dict


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
        error_type: Maps to the `type` field from the Klotty API
    """

    def __init__(
        self,
        code: str,
        error_type: str,
        message: str,
        suggested_action: str = None,
    ):
        Exception.__init__(self, message)
        self.code = code
        self.suggested_action = suggested_action
        self.error_type = error_type


class MissingApiKeyError(KlottyError):
    """see https://klotty.com/docs/errors"""

    def __init__(
        self,
        message,
        error_type,
        code,
    ):
        suggested_action = """Include the following header
        Authorization: Bearer YOUR_API_KEY in the request."""

        KlottyError.__init__(
            self,
            message="Missing API key in the authorization header.",
            suggested_action=suggested_action,
            code=code,
            error_type=error_type,
        )


class InvalidApiKeyError(KlottyError):
    """see https://klotty.com/docs/errors"""

    def __init__(
        self,
        message,
        error_type,
        code,
    ):
        suggested_action = """Generate a new API key in the dashboard."""

        KlottyError.__init__(
            self,
            message=message,
            suggested_action=suggested_action,
            code=code,
            error_type=error_type,
        )


class MissingRequiredFieldsError(KlottyError):
    """see https://klotty.com/docs/errors"""

    def __init__(
        self,
        message,
        error_type,
        code,
    ):
        default_message = """
        The request body is missing one or more required fields."""

        suggested_action = """Check the error message
        to see the list of missing fields."""

        if message != "":
            message = default_message

        KlottyError.__init__(
            self,
            code=code or 422,
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
        )


ERRORS: Dict[str, Dict[str, KlottyError]] = {
    "422": {"missing_required_fields": MissingRequiredFieldsError},
    "401": {"missing_api_key": MissingApiKeyError},
    "403": {"invalid_api_key": InvalidApiKeyError},
}


def raise_for_code_and_type(code, error_type, message: str) -> KlottyError:

    # Handle the case where the error might be unknown
    if ERRORS.get(code).get(error_type) is None:
        raise KlottyError()

    # Raise error from errors list
    error: KlottyError = ERRORS.get(code).get(error_type)
    raise error(code=code, message=message, error_type=error_type)
