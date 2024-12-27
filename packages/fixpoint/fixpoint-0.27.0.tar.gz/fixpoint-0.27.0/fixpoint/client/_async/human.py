"""Asynchronous interface for human-in-the-loop tasks."""

__all__ = ["AsyncHuman"]

from typing import Dict, Optional

from fixpoint_common.types import (
    CreateHumanTaskEntryRequest,
    HumanTaskEntry,
    ListHumanTaskEntriesRequest,
    ListHumanTaskEntriesResponse,
    NodeStatus,
)
from .._common import (
    async_create_human_task,
    async_get_human_task,
    async_list_human_tasks,
)
from ._config import AsyncConfig


class AsyncHuman:
    """Asynchronous interface for human-in-the-loop tasks."""

    _config: AsyncConfig
    _task_entries: "_AsyncHumanTaskEntries"

    def __init__(self, config: AsyncConfig):
        self._config = config
        self._task_entries = _AsyncHumanTaskEntries(config)

    @property
    def task_entries(self) -> "_AsyncHumanTaskEntries":
        """Interface to human-in-the-loop task entries."""
        return self._task_entries


class _AsyncHumanTaskEntries:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(self, task_entry: CreateHumanTaskEntryRequest) -> HumanTaskEntry:
        """Create a human-in-the-loop task entry.

        Args:
            task_entry (HumanTaskEntry): The task entry containing details for the
                human-in-the-loop task.

        Returns:
            HumanTaskEntry: The created human task entry, which includes the
                task details and any additional information provided by the
                system.

        Raises:
            HTTPException: If there's an error in the HTTP request to create the
                task.
        """
        return await async_create_human_task(
            self._config.http_client,
            self._config.core,
            task_entry,
        )

    async def get(self, task_entry_id: str) -> HumanTaskEntry:
        """Get a human-in-the-loop task entry by ID.

        Args:
            task_entry_id (str): The ID of the human-in-the-loop task entry to retrieve.

        Returns:
            HumanTaskEntry: The human task entry.
        """
        return await async_get_human_task(
            self._config.http_client,
            self._config.core,
            task_entry_id,
        )

    async def list(
        self,
        task_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        sampling_size: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status: Optional[NodeStatus] = None,
    ) -> ListHumanTaskEntriesResponse:
        """List all human-in-the-loop task entries for a given task ID.

        Args:
            task_id: (Optional[str]). If provided, list human tasks in the given path.
            workflow_id: (Optional[str]). If provided, filter tasks by this workflow ID.
            workflow_run_id: (Optional[str]). If provided, filter tasks by this workflow run ID.
            sampling_size: (Optional[int]). If provided, limit the number of returned
                tasks to this size, sampled randomly from the list of all tasks
                matching the other filters.
            metadata: (Optional[Dict[str, str]]). If provided, filter tasks by
                matching metadata key-value pairs.

        Returns:
            ListHumanTaskEntriesResponse: A list of human task entries.
        """
        req = ListHumanTaskEntriesRequest(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            sampling_size=sampling_size,
            metadata=metadata,
            status=status,
        )
        return await async_list_human_tasks(
            self._config.http_client,
            self._config.core,
            req,
        )
