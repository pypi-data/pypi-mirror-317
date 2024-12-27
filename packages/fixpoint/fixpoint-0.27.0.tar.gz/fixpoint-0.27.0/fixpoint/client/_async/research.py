"""
Asynchronous interface for interacting with Research Documents, Records, and
Fields.
"""

__all__ = ["AsyncResearch"]

from typing import Dict, Optional

from fixpoint_common.types import (
    CreateResearchRecordRequest,
    ResearchRecord,
    ListResearchRecordsRequest,
    ListResearchRecordsResponse,
    NodeStatus,
)
from .._common import (
    async_create_research_record,
    async_get_research_record,
    async_list_research_records,
)
from ._config import AsyncConfig


class AsyncResearch:
    """Asynchronous interface for Research Documents, Records, and Fields."""

    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config
        self._records = _AsyncResearchRecords(config)

    @property
    def records(self) -> "_AsyncResearchRecords":
        """Async interface to Research Records."""
        return self._records


class _AsyncResearchRecords:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(self, req: CreateResearchRecordRequest) -> ResearchRecord:
        """Create a Research Record.

        Args:
            req (CreateResearchRecordRequest): The request containing details for the
                research record.

        Returns:
            ResearchRecord: The created research record.

        Raises:
            HTTPException: If there's an error in the HTTP request to create the
                research record.
        """
        return await async_create_research_record(
            self._config.http_client,
            self._config.core,
            req,
        )

    async def get(self, document_id: str, record_id: str) -> ResearchRecord:
        """Get a Research Record by document ID and record ID.

        Args:
            document_id (str): The ID of the research document.
            record_id (str): The ID of the research record to retrieve.

        Returns:
            ResearchRecord: The research record.
        """
        return await async_get_research_record(
            self._config.http_client,
            self._config.core,
            document_id,
            record_id,
        )

    async def list(
        self,
        document_id: str,
        workflow_run_id: Optional[str] = None,
        sampling_size: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status: Optional[NodeStatus] = None,
    ) -> ListResearchRecordsResponse:
        """List all Research Records for a given research document ID, with
        additional optional filters.

        Args:
            document_id: (str). The ID of the research document.
            workflow_run_id: (Optional[str]). If provided, filter records by this workflow run ID.
            sampling_size: (Optional[int]). If provided, limit the number of returned
                records to this size, sampled randomly from the list of all records
                matching the other filters.
            metadata: (Optional[Dict[str, str]]). If provided, filter records by
                matching metadata key-value pairs.

        Returns:
            ListResearchRecordsResponse: A list of research records.
        """
        req = ListResearchRecordsRequest(
            research_document_id=document_id,
            workflow_run_id=workflow_run_id,
            sampling_size=sampling_size,
            metadata=metadata,
            status=status,
        )
        return await async_list_research_records(
            self._config.http_client,
            self._config.core,
            req,
        )
