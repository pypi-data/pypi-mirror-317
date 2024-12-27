"""
Synchronous interface for interacting with extractions.
"""

__all__ = ["Extractions"]

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
    create_json_schema_extraction,
    create_record_extraction,
    create_batch_extraction_job,
    get_batch_extraction_job_status,
)
from ._config import Config


class Extractions:
    """Synchronous interface for JSON schema and Record extractions."""

    _config: Config
    _json: "_JsonSchemaExtraction"
    _record: "_RecordExtraction"
    _batch: "_BatchExtraction"

    def __init__(self, config: Config):
        self._config = config
        self._json = _JsonSchemaExtraction(config)
        self._record = _RecordExtraction(config)
        self._batch = _BatchExtraction(config)

    @property
    def json(self) -> "_JsonSchemaExtraction":
        """Sync interface to JSON schema extractions."""
        return self._json

    @property
    def record(self) -> "_RecordExtraction":
        """Sync interface to record extractions."""
        return self._record

    @property
    def batch(self) -> "_BatchExtraction":
        """Sync interface to batch extractions."""
        return self._batch


class _JsonSchemaExtraction:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, req: CreateJsonSchemaExtractionRequest) -> JsonSchemaExtraction:
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
        return create_json_schema_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )


class _RecordExtraction:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, req: CreateRecordExtractionRequest) -> RecordExtraction:
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
        return create_record_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )


class _BatchExtraction:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create_job(self, req: CreateBatchExtractionJobRequest) -> BatchExtractionJob:
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
        return create_batch_extraction_job(
            self._config.http_client,
            self._config.core,
            req,
        )

    def get_job_status(self, job_id: str) -> BatchExtractionJobStatus:
        """Get the status of a batch extraction job.

        Args:
            job_id (str): The ID of the batch extraction job.

        Returns:
            BatchExtractionJobStatus: The status of the batch extraction job.

        Raises:
            FixpointApiError: If there's an error in the HTTP request to get the
                batch extraction job status.
        """
        return get_batch_extraction_job_status(
            self._config.http_client,
            self._config.core,
            job_id,
        )
