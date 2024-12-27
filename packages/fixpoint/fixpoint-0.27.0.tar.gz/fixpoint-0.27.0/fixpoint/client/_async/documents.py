"""Asynchronous interface for interacting with documents."""

__all__ = ["AsyncDocuments"]

from typing import Optional

from fixpoint_common.types import (
    Document,
    ListDocumentsResponse,
)
from ._config import AsyncConfig
from .._common.documents import (
    async_create_document,
    async_get_document,
    async_list_documents,
    async_update_document,
)


class AsyncDocuments:
    """Asynchronous interface for interacting with documents."""

    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def list(
        self,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        task: Optional[str] = None,
        step: Optional[str] = None,
    ) -> ListDocumentsResponse:
        """List documents."""
        return await async_list_documents(
            self._config.http_client,
            self._config.core,
            path=path,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            task=task,
            step=step,
        )

    async def get(
        self,
        doc_id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[Document]:
        """Get a document by ID."""
        return await async_get_document(
            self._config.http_client,
            self._config.core,
            doc_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
        )

    async def create(self, doc: Document) -> Document:
        """Create a document."""
        return await async_create_document(
            self._config.http_client,
            self._config.core,
            doc,
        )

    async def update(self, doc_id: str, doc: Document) -> Document:
        """Update a document."""
        return await async_update_document(
            self._config.http_client,
            self._config.core,
            doc_id,
            doc,
        )
