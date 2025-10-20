from resend import request
from resend.emails._received_email import ReceivedEmail


class Receiving:
    """
    Receiving class that provides methods for retrieving received (inbound) emails.
    """

    @classmethod
    def get(cls, email_id: str) -> ReceivedEmail:
        """
        Retrieve a single received email.
        see more: https://resend.com/docs/api-reference/emails/retrieve-received-email

        Args:
            email_id (str): The ID of the received email to retrieve

        Returns:
            ReceivedEmail: The received email object
        """
        path = f"/emails/receiving/{email_id}"
        resp = request.Request[ReceivedEmail](
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp
