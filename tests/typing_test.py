"""Test that ResponseDict is compatible with TypedDict type hints."""
from typing_extensions import TypedDict

from resend.response import ResponseDict


class EmailResponse(TypedDict):
    """Example typed dict like SendResponse."""
    id: str
    status: str


def test_response_dict_with_typed_dict() -> None:
    """Test that ResponseDict works with TypedDict type hints."""
    # Create a ResponseDict
    data = {"id": "123", "status": "sent"}
    response: EmailResponse = ResponseDict(data, headers={"x-test": "value"})  # type: ignore

    # Type checkers should accept this since ResponseDict is a dict
    assert response["id"] == "123"
    assert response["status"] == "sent"

    # Headers are accessible
    assert isinstance(response, ResponseDict)
    if isinstance(response, ResponseDict):
        assert response.headers["x-test"] == "value"


def returns_typed_dict() -> EmailResponse:
    """Function that returns a TypedDict."""
    return ResponseDict({"id": "456", "status": "delivered"}, headers={"x-id": "abc"})  # type: ignore


def test_function_return_type() -> None:
    """Test that functions can return ResponseDict where TypedDict is expected."""
    result = returns_typed_dict()

    # Works as TypedDict
    assert result["id"] == "456"

    # Can check instance and access headers
    if isinstance(result, ResponseDict):
        assert result.headers["x-id"] == "abc"
