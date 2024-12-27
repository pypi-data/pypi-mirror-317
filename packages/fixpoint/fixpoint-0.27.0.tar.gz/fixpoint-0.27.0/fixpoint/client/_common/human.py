"""Common code for human-in-the-loop tasks."""

__all__ = [
    "create_human_task",
    "async_create_human_task",
    "get_human_task",
    "async_get_human_task",
    "list_human_tasks",
    "async_list_human_tasks",
]

import datetime
import json
from typing import Any, Dict, Union

import httpx

from fixpoint_common.types import (
    CreateHumanTaskEntryRequest,
    HumanTaskEntry,
    ListHumanTaskEntriesRequest,
    ListHumanTaskEntriesResponse,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig


_HUMAN_TASK_ENTRIES_ROUTE = "/human-task-entries"

####
# Create human tasks
####


def create_human_task(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateHumanTaskEntryRequest,
) -> HumanTaskEntry:
    """Make a human task entry"""
    resp = http_client.post(
        config.route_url(_HUMAN_TASK_ENTRIES_ROUTE),
        json=req.model_dump(),
    )
    # only raises if we got an error response
    return _process_task_entry_resp(resp)


async def async_create_human_task(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateHumanTaskEntryRequest,
) -> HumanTaskEntry:
    """Make a synchronous web research scrape request"""
    resp = await http_client.post(
        config.route_url(_HUMAN_TASK_ENTRIES_ROUTE),
        json=req.model_dump(),
    )
    # only raises if we got an error response
    return _process_task_entry_resp(resp)


####
# Get a human task
####


def get_human_task(
    http_client: httpx.Client, config: ApiCoreConfig, task_id: str
) -> HumanTaskEntry:
    """Synchronously get a human task by ID"""
    resp = http_client.get(config.route_url(_HUMAN_TASK_ENTRIES_ROUTE, task_id))
    return _process_task_entry_resp(resp)


async def async_get_human_task(
    http_client: httpx.AsyncClient, config: ApiCoreConfig, task_id: str
) -> HumanTaskEntry:
    """Asynchronously get a human task by ID"""
    resp = await http_client.get(config.route_url(_HUMAN_TASK_ENTRIES_ROUTE, task_id))
    return _process_task_entry_resp(resp)


####
# List human tasks
####


def list_human_tasks(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: ListHumanTaskEntriesRequest,
) -> ListHumanTaskEntriesResponse:
    """Synchronously get a human task by ID"""
    query_params = _new_list_human_tasks_query_params(req)
    resp = http_client.get(
        config.route_url(_HUMAN_TASK_ENTRIES_ROUTE), params=query_params
    )
    return _process_task_entry_list_resp(resp)


async def async_list_human_tasks(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: ListHumanTaskEntriesRequest,
) -> ListHumanTaskEntriesResponse:
    """Asynchronously get a human task by ID"""
    query_params = _new_list_human_tasks_query_params(req)
    resp = await http_client.get(
        config.route_url(_HUMAN_TASK_ENTRIES_ROUTE), params=query_params
    )
    return _process_task_entry_list_resp(resp)


def _new_list_human_tasks_query_params(
    req: ListHumanTaskEntriesRequest,
) -> Dict[str, Union[str, int, float, bool]]:
    query_params: Dict[str, Union[str, int, float, bool]] = {}
    if req.task_id:
        query_params["task_id"] = req.task_id
    if req.workflow_id:
        query_params["workflow_id"] = req.workflow_id
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


def _process_task_entry_json(task_json: Dict[str, Any]) -> HumanTaskEntry:
    obj = HumanTaskEntry.model_validate(task_json)
    _fix_tzinfo(obj)
    return obj


def _fix_tzinfo(hte: HumanTaskEntry) -> None:
    if hte.created_at:
        hte.created_at = hte.created_at.replace(tzinfo=datetime.timezone.utc)
    if hte.updated_at:
        hte.updated_at = hte.updated_at.replace(tzinfo=datetime.timezone.utc)


def _process_task_entry_resp(resp: httpx.Response) -> HumanTaskEntry:
    # only raises if we got an error response
    raise_for_status(resp)
    return _process_task_entry_json(resp.json())


def _process_task_entry_list_resp(resp: httpx.Response) -> ListHumanTaskEntriesResponse:
    # only raises if we got an error response
    raise_for_status(resp)
    response_json = resp.json()
    list_resp = ListHumanTaskEntriesResponse.model_validate(response_json)
    for hte in list_resp.data:
        _fix_tzinfo(hte)
    return list_resp
