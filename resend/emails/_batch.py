from typing import Any, Dict, List, Optional, cast

from typing_extensions import NotRequired, TypedDict

from resend import request

from ._emails import Emails

class SendEmailResponse(TypedDict):
    id: str
    """
    The sent Email ID.
    """

class Batch:

    class SendOptions(TypedDict):
        idempotency_key: NotRequired[str]
        """
        SendOptions is the class that wraps the options for the batch send method.

        Attributes:
            idempotency_key (NotRequired[str]): Unique key that ensures the same operation is not processed multiple times.
            Allows for safe retries without duplicating operations.
            If provided, will be sent as the `Idempotency-Key` header.
        """

    class SendResponse(TypedDict):
        data: List[SendEmailResponse]
        """
        A list of email objects
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
            options (Optional[SendOptions]): Batch options, ie: idempotency_key

        Returns:
            SendResponse: A list of email objects
        """
        path = "/emails/batch"

        resp = request.Request[Batch.SendResponse](
            path=path,
            params=cast(List[Dict[Any, Any]], params),
            verb="post",
            options=cast(Dict[Any, Any], options),
        ).perform_with_content()
        return resp
