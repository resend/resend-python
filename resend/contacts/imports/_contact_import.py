from typing import Optional

from typing_extensions import NotRequired

from resend._base_response import BaseResponse


class ContactImportCounts(BaseResponse):
    """
    ContactImportCounts holds row-level statistics for a contact import.

    Attributes:
        total (int): Total number of rows processed.
        created (int): Number of contacts created.
        updated (int): Number of contacts updated.
        skipped (int): Number of rows skipped.
        failed (int): Number of rows that failed.
    """

    total: int
    created: int
    updated: int
    skipped: int
    failed: int


class ContactImport(BaseResponse):
    """
    ContactImport represents a contact import job.

    Attributes:
        object (str): Always 'contact_import'.
        id (str): Unique identifier for the contact import.
        status (str): 'queued', 'in_progress', 'completed', or 'failed'.
        created_at (str): ISO 8601 timestamp of when the import was created.
        counts (ContactImportCounts): Row-level import statistics (present when status is completed or failed).
    """

    object: str
    id: str
    status: str
    created_at: str
    completed_at: Optional[str]
    counts: NotRequired[ContactImportCounts]
