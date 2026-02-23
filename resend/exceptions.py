"""Resend Exceptions module.

This module defines the base types for platform-wide error
codes as outlined in https://resend.com/docs/api-reference/errors.
"""

from typing import Any, Dict, NoReturn, Optional, Union


class ResendError(Exception):
    """Base class for all errors raised by Resend SDK.
    This is the parent class of all exceptions (server side)
    raised by the Resend SDK. Developers can simply catch
    this class and inspect its `code` to implement more specific
    error handling. Note that for some client-side errors ie:
    some method argument missing, a ValueError would be raised.

    Args:
        code: A string error indicating the HTTP status code
        attributed to that Error.
        message: A human-readable error message string.
        suggested_action: A suggested action path to help the user.
        error_type: Maps to the `type` field from the Resend API
    """

    def __init__(
        self,
        code: Union[str, int],
        error_type: str,
        message: str,
        suggested_action: str,
        headers: Optional[Dict[str, str]] = None,
    ):
        Exception.__init__(self, message)
        self.code = code
        self.message = message
        self.suggested_action = suggested_action
        self.error_type = error_type
        self.headers = headers or {}


class MissingApiKeyError(ResendError):
    """see https://resend.com/docs/api-reference/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
        headers: Optional[Dict[str, str]] = None,
    ):
        suggested_action = """Include the following header
        Authorization: Bearer YOUR_API_KEY in the request."""

        message = "Missing API key in the authorization header."

        ResendError.__init__(
            self,
            message=message,
            suggested_action=suggested_action,
            code=code,
            error_type=error_type,
            headers=headers,
        )


class InvalidApiKeyError(ResendError):
    """see https://resend.com/docs/api-reference/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
        headers: Optional[Dict[str, str]] = None,
    ):
        suggested_action = """Generate a new API key in the dashboard."""

        ResendError.__init__(
            self,
            message=message,
            suggested_action=suggested_action,
            code=code,
            error_type=error_type,
            headers=headers,
        )


class ValidationError(ResendError):
    """see https://resend.com/docs/api-reference/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
        headers: Optional[Dict[str, str]] = None,
    ):
        default_message = """
        The request body is missing one or more required fields."""

        suggested_action = """Check the error message
        to see the list of missing fields."""

        if message == "":
            message = default_message

        ResendError.__init__(
            self,
            code=code or "400",
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
            headers=headers,
        )


class MissingRequiredFieldsError(ResendError):
    """see https://resend.com/docs/api-reference/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
        headers: Optional[Dict[str, str]] = None,
    ):
        default_message = """
        The request body is missing one or more required fields."""

        suggested_action = """Check the error message
        to see the list of missing fields."""

        if message == "":
            message = default_message

        ResendError.__init__(
            self,
            code=code or "422",
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
            headers=headers,
        )


class ApplicationError(ResendError):
    """see https://resend.com/docs/api-reference/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
        headers: Optional[Dict[str, str]] = None,
    ):
        default_message = """
        Something went wrong."""

        suggested_action = """Contact Resend support."""

        if message == "":
            message = default_message

        ResendError.__init__(
            self,
            code=code or "500",
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
            headers=headers,
        )


class RateLimitError(ResendError):
    """see https://resend.com/docs/api-reference/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
        headers: Optional[Dict[str, str]] = None,
    ):
        suggested_action = """Reduce your request rate or wait before retrying. """
        suggested_action += """Check the response headers for rate limit information."""

        ResendError.__init__(
            self,
            code=code or "429",
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
            headers=headers,
        )


# Dict with error code -> error type mapping
ERRORS: Dict[str, Dict[str, Any]] = {
    "400": {"validation_error": ValidationError},
    "422": {
        "missing_required_fields": MissingRequiredFieldsError,
        "validation_error": ValidationError,
    },
    "401": {"missing_api_key": MissingApiKeyError},
    "403": {"invalid_api_key": InvalidApiKeyError},
    "429": {
        "rate_limit_exceeded": RateLimitError,
        "daily_quota_exceeded": RateLimitError,
        "monthly_quota_exceeded": RateLimitError,
    },
    "500": {"application_error": ApplicationError},
}


def raise_for_code_and_type(
    code: Union[str, int],
    error_type: str,
    message: str,
    headers: Optional[Dict[str, str]] = None,
) -> NoReturn:
    """Raise the appropriate error based on the code and type.

    Args:
        code (str): The error code
        error_type (str): The error type
        message (str): The error message
        headers (Optional[Dict[str, str]]): The HTTP response headers

    Raises:
        ResendError: If it is a Resend err
            or
        ValidationError: If the error type is validation_error
            or
        MissingRequiredFieldsError: If the error type is missing_required_fields
            or
        MissingApiKeyError: If the error type is missing_api_key
            or
        InvalidApiKeyError: If the error type is invalid_api_key
            or
        RateLimitError: If the error type is rate_limit_exceeded, daily_quota_exceeded, or monthly_quota_exceeded
            or
        ApplicationError: If the error type is application_error
            or
        TypeError: If the error type is not found
    """
    error = ERRORS.get(str(code))

    # Handle the case where the error might be unknown
    if error is None:
        raise ResendError(
            code=code,
            message=message,
            error_type=error_type,
            suggested_action="",
            headers=headers,
        )

    # Raise error from errors list
    error_from_list = error.get(error_type)

    if error_from_list is not None:
        raise error_from_list(
            code=code,
            message=message,
            error_type=error_type,
            headers=headers,
        )
    # defaults to ResendError if finally can't find error type
    raise ResendError(
        code=code,
        message=message,
        error_type=error_type,
        suggested_action="",
        headers=headers,
    )


class NoContentError(Exception):
    """Raised when the response body is empty."""

    def __init__(self) -> None:
        self.message = """No content was returned from the API.
            Please contact Resend support."""
        Exception.__init__(self, self.message)
