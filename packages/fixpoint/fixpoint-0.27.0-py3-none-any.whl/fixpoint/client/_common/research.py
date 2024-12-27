"""Common code for Research Documents, Records, and Fields."""

__all__ = [
    "create_research_record",
    "async_create_research_record",
    "get_research_record",
    "async_get_research_record",
    "list_research_records",
    "async_list_research_records",
]

import datetime
import json
from typing import Any, Dict, Union, Optional

import httpx

from fixpoint_common.types import (
    CreateResearchRecordRequest,
    ResearchRecord,
    ListResearchRecordsRequest,
    ListResearchRecordsResponse,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig


_RESEARCH_ROUTE = "/research"


def _new_route_url(document_id: str, record_id: Optional[str] = None) -> str:
    parts = [_RESEARCH_ROUTE, "documents", document_id, "records"]
    if record_id:
        parts.append(record_id)
    return "/".join(parts)


####
# Create research records
####


def create_research_record(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateResearchRecordRequest,
) -> ResearchRecord:
    """Create a research record"""
    resp = http_client.post(
        config.route_url(_new_route_url(document_id=req.research_document_id)),
        json=req.model_dump(),
    )
    # only raises if we got an error response
    return _process_research_record_resp(resp)


async def async_create_research_record(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateResearchRecordRequest,
) -> ResearchRecord:
    """Create a research record"""
    resp = await http_client.post(
        config.route_url(_new_route_url(document_id=req.research_document_id)),
        json=req.model_dump(),
    )
    # only raises if we got an error response
    return _process_research_record_resp(resp)


####
# Get a Research Record
####


def get_research_record(
    http_client: httpx.Client, config: ApiCoreConfig, document_id: str, record_id: str
) -> ResearchRecord:
    """Synchronously get a research record by ID"""
    resp = http_client.get(
        config.route_url(_new_route_url(document_id=document_id, record_id=record_id))
    )
    return _process_research_record_resp(resp)


async def async_get_research_record(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    document_id: str,
    record_id: str,
) -> ResearchRecord:
    """Asynchronously get a research record by ID"""
    resp = await http_client.get(
        config.route_url(_new_route_url(document_id=document_id, record_id=record_id))
    )
    return _process_research_record_resp(resp)


####
# List Research Records
####


def list_research_records(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: ListResearchRecordsRequest,
) -> ListResearchRecordsResponse:
    """Synchronously list Research Records belonging to a document"""
    query_params = _new_list_research_records_query_params(req)
    resp = http_client.get(
        config.route_url(_new_route_url(document_id=req.research_document_id)),
        params=query_params,
    )
    return _process_research_record_list_resp(resp)


async def async_list_research_records(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: ListResearchRecordsRequest,
) -> ListResearchRecordsResponse:
    """Asynchronously list Research Records belonging to a document"""
    query_params = _new_list_research_records_query_params(req)
    resp = await http_client.get(
        config.route_url(_new_route_url(document_id=req.research_document_id)),
        params=query_params,
    )
    return _process_research_record_list_resp(resp)


def _new_list_research_records_query_params(
    req: ListResearchRecordsRequest,
) -> Dict[str, Union[str, int, float, bool]]:
    query_params: Dict[str, Union[str, int, float, bool]] = {
        "document_id": req.research_document_id,
    }
    if req.workflow_run_id:
        query_params["workflow_run_id"] = req.workflow_run_id
    if req.sampling_size:
        query_params["sampling_size"] = req.sampling_size
    if req.metadata:
        query_params["metadata"] = json.dumps(req.metadata)
    if req.status:
        query_params["status"] = req.status.value

    return query_params


####
# Helpers
####


def _process_research_record_json(record_json: Dict[str, Any]) -> ResearchRecord:
    obj = ResearchRecord.model_validate(record_json)
    _fix_tzinfo(obj)
    return obj


def _fix_tzinfo(record: ResearchRecord) -> None:
    if record.created_at:
        record.created_at = record.created_at.replace(tzinfo=datetime.timezone.utc)
    if record.updated_at:
        record.updated_at = record.updated_at.replace(tzinfo=datetime.timezone.utc)


def _process_research_record_resp(resp: httpx.Response) -> ResearchRecord:
    # only raises if we got an error response
    raise_for_status(resp)
    return _process_research_record_json(resp.json())


def _process_research_record_list_resp(
    resp: httpx.Response,
) -> ListResearchRecordsResponse:
    # only raises if we got an error response
    raise_for_status(resp)
    response_json = resp.json()
    list_resp = ListResearchRecordsResponse.model_validate(response_json)
    for record in list_resp.data:
        _fix_tzinfo(record)
    return list_resp
