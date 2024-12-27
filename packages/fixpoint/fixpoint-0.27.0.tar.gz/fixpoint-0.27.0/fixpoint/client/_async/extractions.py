"""
Asynchronous interface for interacting with extractions.
"""

__all__ = ["AsyncExtractions"]

from typing import Dict, Optional
from fixpoint_common.types import (
    CreateJsonSchemaExtractionRequest,
    JsonSchemaExtraction,
    CreateRecordExtractionRequest,
    RecordExtraction,
)
from fixpoint_common.types.extraction import (
    CreateBatchExtractionJobRequest,
    BatchExtractionJob,
    BatchExtractionJobStatus,
)
from .._common.extraction import (
    async_create_json_schema_extraction,
    async_create_record_extraction,
    async_create_batch_extraction_job,
    async_get_batch_extraction_job_status,
)
from ._config import AsyncConfig


class AsyncExtractions:
    """Asynchronous interface for JSON schema and Record extractions."""

    _config: AsyncConfig
    _json: "_AsyncJsonSchemaExtraction"
    _record: "_AsyncRecordExtraction"
    _batch: "_AsyncBatchExtraction"

    def __init__(self, config: AsyncConfig):
        self._config = config
        self._json = _AsyncJsonSchemaExtraction(config)
        self._record = _AsyncRecordExtraction(config)
        self._batch = _AsyncBatchExtraction(config)

    @property
    def json(self) -> "_AsyncJsonSchemaExtraction":
        """Async interface to JSON schema extractions."""
        return self._json

    @property
    def record(self) -> "_AsyncRecordExtraction":
        """Async interface to record extractions."""
        return self._record

    @property
    def batch(self) -> "_AsyncBatchExtraction":
        """Async interface to batch extractions."""
        return self._batch


class _AsyncJsonSchemaExtraction:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(
        self, req: CreateJsonSchemaExtractionRequest
    ) -> JsonSchemaExtraction:
        """Create a JSON schema extraction.

        Args:
            req (CreateJsonSchemaExtractionRequest): The request containing details for the
                JSON schema extraction.

        Returns:
            JsonSchemaExtraction: The created JSON schema extraction.

        Raises:
            FixpointApiError: If there's an error in the HTTP request to create the
                JSON schema extraction.
        """
        return await async_create_json_schema_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )


class _AsyncRecordExtraction:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(
        self,
        req: CreateRecordExtractionRequest,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> RecordExtraction:
        """Create a record extraction.

        Args:
            req (CreateRecordExtractionRequest): The request containing details for the
                record extraction.

        Returns:
            RecordExtraction: The created record extraction.

        Raises:
            FixpointApiError: If there's an error in the HTTP request to create the
                record extraction.
        """
        return await async_create_record_extraction(
            self._config.http_client,
            self._config.core,
            req,
            additional_headers=additional_headers,
        )


class _AsyncBatchExtraction:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create_job(
        self, req: CreateBatchExtractionJobRequest
    ) -> BatchExtractionJob:
        """Create a batch extraction job.

        Args:
            req (CreateBatchExtractionJobRequest): The request containing details for the
                batch extraction job.

        Returns:
            BatchExtractionJob: The created batch extraction job.

        Raises:
            FixpointApiError: If there's an error in the HTTP request to create the
                batch extraction job.
        """
        return await async_create_batch_extraction_job(
            self._config.http_client,
            self._config.core,
            req,
        )

    async def get_job_status(self, job_id: str) -> BatchExtractionJobStatus:
        """Get the status of a batch extraction job.

        Args:
            job_id (str): The ID of the batch extraction job.

        Returns:
            BatchExtractionJobStatus: The status of the batch extraction job.

        Raises:
            FixpointApiError: If there's an error in the HTTP request to get the
                batch extraction job status.
        """
        return await async_get_batch_extraction_job_status(
            self._config.http_client,
            self._config.core,
            job_id,
        )
