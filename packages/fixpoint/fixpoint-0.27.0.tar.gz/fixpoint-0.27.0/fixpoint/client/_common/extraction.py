"""
Common extraction functions.
"""

__all__ = [
    "async_create_json_schema_extraction",
    "create_json_schema_extraction",
    "async_create_record_extraction",
    "create_record_extraction",
]

import os
from typing import Dict, Optional
import httpx

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
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig


_EXTRACTION_ROUTE = "/extractions"
_JSON_EXTRACTION_ROUTE = f"{_EXTRACTION_ROUTE}/json_schema_extractions"
_RECORD_EXTRACTION_ROUTE = f"{_EXTRACTION_ROUTE}/record_extractions"
_BATCH_EXTRACTION_JOBS_ROUTE = f"{_EXTRACTION_ROUTE}/batch_extraction_jobs"


def _batch_job_status_route(job_id: str) -> str:
    return os.path.join(_BATCH_EXTRACTION_JOBS_ROUTE, job_id, "status")


async def async_create_json_schema_extraction(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateJsonSchemaExtractionRequest,
) -> JsonSchemaExtraction:
    """Create a JSON schema extraction."""
    resp = await http_client.post(
        config.route_url(_JSON_EXTRACTION_ROUTE),
        # without `by_alias=True`, the `schema` field is serialized as
        # `schema_`
        json=req.model_dump(by_alias=True),
        timeout=None,
    )
    return _process_json_schema_extraction_resp(resp)


def create_json_schema_extraction(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateJsonSchemaExtractionRequest,
) -> JsonSchemaExtraction:
    """Create a JSON schema extraction."""
    resp = http_client.post(
        config.route_url(_JSON_EXTRACTION_ROUTE),
        # without `by_alias=True`, the `schema` field is serialized as
        # `schema_`
        json=req.model_dump(by_alias=True),
        timeout=None,
    )
    return _process_json_schema_extraction_resp(resp)


def _process_json_schema_extraction_resp(resp: httpx.Response) -> JsonSchemaExtraction:
    raise_for_status(resp)
    return JsonSchemaExtraction.model_validate(resp.json())


async def async_create_record_extraction(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateRecordExtractionRequest,
    additional_headers: Optional[Dict[str, str]] = None,
) -> RecordExtraction:
    """Create a record extraction."""
    resp = await http_client.post(
        config.route_url(_RECORD_EXTRACTION_ROUTE),
        json=req.model_dump(),
        headers=additional_headers or {},
    )
    return _process_record_extraction_resp(resp)


def create_record_extraction(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateRecordExtractionRequest,
    additional_headers: Optional[Dict[str, str]] = None,
) -> RecordExtraction:
    """Create a record extraction."""
    resp = http_client.post(
        config.route_url(_RECORD_EXTRACTION_ROUTE),
        json=req.model_dump(),
        headers=additional_headers or {},
    )
    return _process_record_extraction_resp(resp)


def _process_record_extraction_resp(resp: httpx.Response) -> RecordExtraction:
    raise_for_status(resp)
    return RecordExtraction.model_validate(resp.json())


def create_batch_extraction_job(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateBatchExtractionJobRequest,
) -> BatchExtractionJob:
    """Create a batch extraction job."""
    resp = http_client.post(
        config.route_url(_BATCH_EXTRACTION_JOBS_ROUTE),
        json=req.model_dump(),
    )
    return _process_batch_extraction_job_resp(resp)


async def async_create_batch_extraction_job(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateBatchExtractionJobRequest,
) -> BatchExtractionJob:
    """Async create a batch extraction job."""
    resp = await http_client.post(
        config.route_url(_BATCH_EXTRACTION_JOBS_ROUTE),
        json=req.model_dump(),
    )
    return _process_batch_extraction_job_resp(resp)


def _process_batch_extraction_job_resp(resp: httpx.Response) -> BatchExtractionJob:
    raise_for_status(resp)
    return BatchExtractionJob.model_validate(resp.json())


def get_batch_extraction_job_status(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    job_id: str,
) -> BatchExtractionJobStatus:
    """Get the status of a batch extraction job."""
    resp = http_client.get(config.route_url(_batch_job_status_route(job_id)))
    return _process_batch_extraction_job_status_resp(resp)


async def async_get_batch_extraction_job_status(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    job_id: str,
) -> BatchExtractionJobStatus:
    """Async get the status of a batch extraction job."""
    resp = await http_client.get(config.route_url(_batch_job_status_route(job_id)))
    return _process_batch_extraction_job_status_resp(resp)


def _process_batch_extraction_job_status_resp(
    resp: httpx.Response,
) -> BatchExtractionJobStatus:
    raise_for_status(resp)
    return BatchExtractionJobStatus.model_validate(resp.json())
