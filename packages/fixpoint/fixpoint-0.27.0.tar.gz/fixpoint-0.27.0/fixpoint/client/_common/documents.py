"""Common code for interacting with documents."""

__all__ = [
    "list_documents",
    "async_list_documents",
    "get_document",
    "async_get_document",
    "create_document",
    "async_create_document",
    "update_document",
    "async_update_document",
]

from typing import Optional, Dict, Any

import httpx

from fixpoint_common.types import (
    ListDocumentsResponse,
    Document,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig

_DOCUMENTS_ROUTE = "/documents"


def list_documents(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    path: Optional[str] = None,
    workflow_id: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
    task: Optional[str] = None,
    step: Optional[str] = None,
) -> ListDocumentsResponse:
    """Make a synchronous web research scrape request"""
    resp = http_client.get(
        config.route_url(_DOCUMENTS_ROUTE),
        params=_create_params(
            {
                "path": path,
                "workflow_id": workflow_id,
                "workflow_run_id": workflow_run_id,
                "task": task,
                "step": step,
            }
        ),
    )
    # only raises if we got an error response
    return _process_list_docs_response(resp)


async def async_list_documents(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    path: Optional[str] = None,
    workflow_id: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
    task: Optional[str] = None,
    step: Optional[str] = None,
) -> ListDocumentsResponse:
    """Make a synchronous web research scrape request"""
    resp = await http_client.get(
        config.route_url(_DOCUMENTS_ROUTE),
        params=_create_params(
            {
                "path": path,
                "workflow_id": workflow_id,
                "workflow_run_id": workflow_run_id,
                "task": task,
                "step": step,
            }
        ),
    )
    # only raises if we got an error response
    return _process_list_docs_response(resp)


def get_document(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    doc_id: str,
    workflow_id: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
) -> Optional[Document]:
    """Make a synchronous request to get a document by ID"""
    resp = http_client.get(
        config.route_url(f"{_DOCUMENTS_ROUTE}/{doc_id}"),
        params=_create_params(
            {
                "workflow_id": workflow_id,
                "workflow_run_id": workflow_run_id,
            }
        ),
    )
    return _process_maybe_document_resp(resp)


async def async_get_document(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    doc_id: str,
    workflow_id: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
) -> Optional[Document]:
    """Make an asynchronous request to get a document by ID"""
    resp = await http_client.get(
        config.route_url(f"{_DOCUMENTS_ROUTE}/{doc_id}"),
        params=_create_params(
            {
                "workflow_id": workflow_id,
                "workflow_run_id": workflow_run_id,
            }
        ),
    )
    return _process_maybe_document_resp(resp)


def create_document(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    doc: Document,
) -> Document:
    """Make a synchronous request to create a document"""
    resp = http_client.post(
        config.route_url(_DOCUMENTS_ROUTE),
        json=doc.model_dump(),
    )
    return _process_document_resp(resp)


async def async_create_document(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    doc: Document,
) -> Document:
    """Make an asynchronous request to create a document"""
    resp = await http_client.post(
        config.route_url(_DOCUMENTS_ROUTE),
        json=doc.model_dump(),
    )
    return _process_document_resp(resp)


def update_document(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    doc_id: str,
    doc: Document,
) -> Document:
    """Make a synchronous request to update a document"""
    resp = http_client.put(
        config.route_url(f"{_DOCUMENTS_ROUTE}/{doc_id}"),
        json=doc.model_dump(),
    )
    return _process_document_resp(resp)


async def async_update_document(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    doc_id: str,
    doc: Document,
) -> Document:
    """Make an asynchronous request to update a document"""
    resp = await http_client.put(
        config.route_url(f"{_DOCUMENTS_ROUTE}/{doc_id}"),
        json=doc.model_dump(),
    )
    return _process_document_resp(resp)


def _create_params(params: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}


def _process_maybe_document_resp(resp: httpx.Response) -> Optional[Document]:
    raise_for_status(resp)
    jsobj = resp.json()
    if jsobj is None:
        return None
    return Document.model_validate(jsobj)


def _process_document_resp(resp: httpx.Response) -> Document:
    raise_for_status(resp)
    jsobj = resp.json()
    return Document.model_validate(jsobj)


def _process_list_docs_response(resp: httpx.Response) -> ListDocumentsResponse:
    raise_for_status(resp)
    jsobj = resp.json()
    return ListDocumentsResponse.model_validate(jsobj)
