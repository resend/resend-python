"""Resend Exceptions module.

This module defines the base types for platform-wide error
codes as outlined in https://resend.com/docs/errors.
"""

from typing import Any, Dict, Union


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
    ):
        Exception.__init__(self, message)
        self.code = code
        self.message = message
        self.suggested_action = suggested_action
        self.error_type = error_type


class MissingApiKeyError(ResendError):
    """see https://resend.com/docs/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
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
        )


class InvalidApiKeyError(ResendError):
    """see https://resend.com/docs/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
    ):
        suggested_action = """Generate a new API key in the dashboard."""

        ResendError.__init__(
            self,
            message=message,
            suggested_action=suggested_action,
            code=code,
            error_type=error_type,
        )


class ValidationError(ResendError):
    """see https://resend.com/docs/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
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
        )


class MissingRequiredFieldsError(ResendError):
    """see https://resend.com/docs/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
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
        )


class ApplicationError(ResendError):
    """see https://resend.com/docs/errors"""

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
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
    "500": {"application_error": ApplicationError},
}


def raise_for_code_and_type(
    code: Union[str, int], error_type: str, message: str
) -> None:
    """Raise the appropriate error based on the code and type.

    Args:
        code (str): The error code
        error_type (str): The error type
        message (str): The error message

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
        ApplicationError: If the error type is application_error
            or
        TypeError: If the error type is not found
    """
    error = ERRORS.get(str(code))

    # Handle the case where the error might be unknown
    if error is None:
        raise ResendError(
            code=code, message=message, error_type=error_type, suggested_action=""
        )

    # Raise error from errors list
    error_from_list = error.get(error_type)

    if error_from_list is not None:
        raise error_from_list(
            code=code,
            message=message,
            error_type=error_type,
        )
    # defaults to ResendError if finally can't find error type
    raise ResendError(
        code=code, message=message, error_type=error_type, suggested_action=""
    )
