from typing import Any, Dict, List, Optional, cast

from typing_extensions import Literal, NotRequired, TypedDict

from resend import request

from ._emails import Emails


class SendEmailResponse(TypedDict):
    id: str
    """
    The sent Email ID.
    """


class BatchValidationError(TypedDict):
    """
    BatchValidationError represents a validation error for a specific email in the batch.

    Attributes:
        index (int): The index of the email in the batch that caused the error
        message (str): The validation error message
    """

    index: int
    """
    The index of the email in the batch that caused the error.
    """
    message: str
    """
    The validation error message.
    """


class Batch:

    class SendOptions(TypedDict):
        """
        SendOptions is the class that wraps the options for the batch send method.

        Attributes:
            idempotency_key (NotRequired[str]): Unique key that ensures the same operation is not processed multiple times.
            Allows for safe retries without duplicating operations.
            If provided, will be sent as the `Idempotency-Key` header.
            batch_validation (NotRequired[Literal["strict", "permissive"]]): Batch validation mode.
            Defaults to "strict" when not provided.
        """

        idempotency_key: NotRequired[str]
        """
        Unique key that ensures the same operation is not processed multiple times.
        Allows for safe retries without duplicating operations.
        If provided, will be sent as the `Idempotency-Key` header.
        """

        batch_validation: NotRequired[Literal["strict", "permissive"]]
        """
        Batch validation mode.
        Defaults to "strict" when not provided.
        """

    class SendResponse(TypedDict):
        data: List[SendEmailResponse]
        """
        A list of email objects
        """
        errors: NotRequired[List[BatchValidationError]]
        """
        A list of validation errors (only present in permissive mode)
        """

    @classmethod
    def send(
        cls, params: List[Emails.SendParams], options: Optional[SendOptions] = None
    ) -> SendResponse:
        """
        Trigger up to 100 batch emails at once.
        see more: https://resend.com/docs/api-reference/emails/send-batch-emails

        Args:
            params (List[Emails.SendParams]): The list of emails to send
            options (Optional[SendOptions]): Batch options, including batch_validation mode

        Returns:
            SendResponse: A list of email objects, and optionally validation errors in permissive mode
        """
        path = "/emails/batch"

        resp = request.Request[Batch.SendResponse](
            path=path,
            params=cast(List[Dict[Any, Any]], params),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp
