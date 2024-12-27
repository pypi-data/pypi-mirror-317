"""Asynchronous interface for interacting with workflows."""

from typing import Any, Dict, Optional, Sequence

from fixpoint_common.types.basic import AsyncFunc, Params, Ret_co
from fixpoint_common.constants import NO_AUTH_ORG_ID
from fixpoint_common.workflows.structured import (
    run_workflow,
    retry_workflow,
    spawn_workflow,
    respawn_workflow,
    WorkflowRunHandle,
)
from ._config import AsyncConfig


class AsyncWorkflows:
    """Asynchronous interface for interacting with workflows."""

    _config: AsyncConfig
    _structured: "StructuredWorkflows"

    def __init__(self, config: AsyncConfig):
        self._config = config
        self._structured = StructuredWorkflows(config)

    @property
    def structured(self) -> "StructuredWorkflows":
        """Interface to structured workflows."""
        return self._structured


class StructuredWorkflows:
    """Asynchronous interface for interacting with structured workflows."""

    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def run(
        self,
        workflow_entry: AsyncFunc[Params, Ret_co],
        *,
        run_id: Optional[str] = None,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Ret_co:
        """Runs a structured workflow, returning its result.

        If you pass in a run_id, that is used as an idempotency key for all
        durability functions, and it also identifies the workflow run.

        This is a shortcut for `client.workflows.structured.spawn(...).result()`.
        """
        if run_id is not None:
            return await self.retry(
                workflow_entry, run_id=run_id, args=args, kwargs=kwargs
            )

        res = await run_workflow(
            workflow_entry,
            # Because the run_config uses the an API client, which in turn
            # ignores the org_id and grabs it off the API key, we can pass in
            # the no-auth org ID here.
            org_id=NO_AUTH_ORG_ID,
            run_config=self._config.core.run_config,
            args=args,
            kwargs=kwargs,
        )
        return res

    async def retry(
        self,
        workflow_entry: AsyncFunc[Params, Ret_co],
        *,
        run_id: str,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Ret_co:
        """Retries a workflow run, skipping past completed tasks and steps.

        The run_id is the ID of the workflow run to retry.

        This is a shortcut for `client.workflows.structured.respawn(...).result()`.
        """
        res = await retry_workflow(
            workflow_entry,
            # Because the run_config uses the an API client, which in turn
            # ignores the org_id and grabs it off the API key, we can pass in
            # the no-auth org ID here.
            org_id=NO_AUTH_ORG_ID,
            run_id=run_id,
            run_config=self._config.core.run_config,
            args=args,
            kwargs=kwargs,
        )
        return res

    def spawn(
        self,
        workflow_entry: AsyncFunc[Params, Ret_co],
        *,
        run_id: Optional[str] = None,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> WorkflowRunHandle[Ret_co]:
        """Spawns a structured workflow.

        If you pass in a run_id, that is used as an idempotency key for all
        durability functions, and it also identifies the workflow run.

        A workflow begins with a class decorated with
        `@structured.workflow(...)`.

        A more complete example:

        ```
        @structured.workflow(id="my-workflow")
        class MyWorkflow:
            @structured.workflow_entrypoint()
            def main(self, ctx: WorkflowContext, args: Dict[str, Any]) -> None:
                ...


        client.workflows.structured.spawn(
            MyWorkflow.main,
            args=[{"somevalue": "foobar"}]
        )
        ```
        """
        if run_id is not None:
            return self.respawn(workflow_entry, run_id=run_id, args=args, kwargs=kwargs)

        handle = spawn_workflow(
            workflow_entry,
            # Because the run_config uses the an API client, which in turn
            # ignores the org_id and grabs it off the API key, we can pass in
            # the no-auth org ID here.
            org_id=NO_AUTH_ORG_ID,
            run_config=self._config.core.run_config,
            args=args,
            kwargs=kwargs,
        )
        return handle

    def respawn(
        self,
        workflow_entry: AsyncFunc[Params, Ret_co],
        *,
        run_id: str,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> WorkflowRunHandle[Ret_co]:
        """Retries spawning a structured workflow."""
        handle = respawn_workflow(
            workflow_entry,
            # Because the run_config uses the an API client, which in turn
            # ignores the org_id and grabs it off the API key, we can pass in
            # the no-auth org ID here.
            org_id=NO_AUTH_ORG_ID,
            run_id=run_id,
            run_config=self._config.core.run_config,
            args=args,
            kwargs=kwargs,
        )
        return handle
