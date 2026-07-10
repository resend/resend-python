from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import Literal, NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse

from ._emails import Emails

# Async imports (optional - only available with pip install resend[async])
try:
    from resend.async_request import AsyncRequest
except ImportError:
    pass


class SendEmailResponse(BaseResponse):
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

    class SendParams(Emails.SendParams):
        """SendParams is the class that wraps the parameters for each email in a batch send.

        Attributes:
            from (NotRequired[str]): The email address to send the email from.
            to (Union[str, List[str]]): List of email addresses to send the email to.
            subject (NotRequired[str]): The subject of the email.
            bcc (NotRequired[Union[List[str], str]]): Bcc
            cc (NotRequired[Union[List[str], str]]): Cc
            reply_to (NotRequired[Union[List[str], str]]): Reply to
            html (NotRequired[str]): The HTML content of the email.
            text (NotRequired[str]): The text content of the email.
            headers (NotRequired[Dict[str, str]]): Custom headers to be added to the email.
            attachments (NotRequired[List[Union[Attachment, RemoteAttachment]]]): List of attachments to be added to the email.
            tags (NotRequired[List[Tag]]): List of tags to be added to the email.
            scheduled_at (NotRequired[str]): Schedule email to be sent later.
            The date should be in ISO 8601 format (e.g: 2024-08-05T11:52:01.858Z).
            template (NotRequired[EmailTemplate]): Template configuration for sending emails using predefined templates.
        """

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

    class SendResponse(BaseResponse):
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
        cls, params: List[SendParams], options: Optional[SendOptions] = None
    ) -> SendResponse:
        """
        Trigger up to 100 batch emails at once.
        see more: https://resend.com/docs/api-reference/emails/send-batch-emails

        Args:
            params (List[SendParams]): The list of emails to send
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

    @classmethod
    async def send_async(
        cls, params: List[SendParams], options: Optional[SendOptions] = None
    ) -> SendResponse:
        """
        Trigger up to 100 batch emails at once (async).
        see more: https://resend.com/docs/api-reference/emails/send-batch-emails

        Args:
            params (List[SendParams]): The list of emails to send
            options (Optional[SendOptions]): Batch options, ie: idempotency_key

        Returns:
            SendResponse: A list of email objects
        """
        path = "/emails/batch"

        resp = await AsyncRequest[Batch.SendResponse](
            path=path,
            params=cast(List[Dict[Any, Any]], params),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp
