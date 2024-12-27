"""Synchronous interface for human-in-the-loop tasks."""

__all__ = ["Human"]

from typing import Dict, Optional

from fixpoint_common.types import (
    CreateHumanTaskEntryRequest,
    HumanTaskEntry,
    ListHumanTaskEntriesRequest,
    ListHumanTaskEntriesResponse,
    NodeStatus,
)
from .._common import create_human_task, get_human_task, list_human_tasks
from ._config import Config


class Human:
    """Synchronous interface for human-in-the-loop tasks."""

    _config: Config
    _task_entries: "_HumanTaskEntries"

    def __init__(self, config: Config):
        self._config = config
        self._task_entries = _HumanTaskEntries(config)

    @property
    def task_entries(self) -> "_HumanTaskEntries":
        """Interface to human-in-the-loop task entries."""
        return self._task_entries


class _HumanTaskEntries:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, task_entry: CreateHumanTaskEntryRequest) -> HumanTaskEntry:
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
                task entry.
        """
        return create_human_task(
            self._config.http_client,
            self._config.core,
            task_entry,
        )

    def get(self, task_entry_id: str) -> HumanTaskEntry:
        """Get a human-in-the-loop task entry by ID.

        Args:
            task_entry_id (str): The ID of the human-in-the-loop task entry to
                retrieve.

        Returns:
            HumanTaskEntry: The human task entry.
        """
        return get_human_task(
            self._config.http_client,
            self._config.core,
            task_entry_id,
        )

    def list(
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
            req (Optional[ListHumanTaskEntriesRequest]): The request object containing
                optional query filters for the list of human tasks.

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
        return list_human_tasks(
            self._config.http_client,
            self._config.core,
            req,
        )
