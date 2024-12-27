"""Synchronous Fixpoint agents."""

from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel
from pydantic_core import Url

from fixpoint_common.completions import ChatCompletionMessageParam
from fixpoint_common.webresearcher import (
    AllResearchResultsPydantic as AllResearchResults,
    CreateScrapeRequest,
)
from .._common import webresearch_scrape
from ._config import Config


BM = TypeVar("BM", bound=BaseModel)


class Agents:
    """Interface to various synchronous Fixpoint agents."""

    _config: Config
    webresearcher: "WebResearcher"

    def __init__(self, config: Config):
        self._config = config
        self.webresearcher = WebResearcher(config)


class WebResearcher:
    """Interface to the synchronous WebResearcher agent."""

    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def scrape(
        self,
        workflow_id: str,
        site: str,
        research_schema: Type[BM],
        run_id: Optional[str] = None,
        extra_instructions: Optional[List[ChatCompletionMessageParam]] = None,
    ) -> AllResearchResults[BM]:
        """Spawn a workflow to scrape a list of sites and extract the research results.

        Args:
            run_config (RunConfig): Configuration for the workflow run.
            clients (Clients): Client instances for external services.
            workflow_id (str): Unique identifier for the workflow.
            site (str): URL to scrape.
            research_schema (Type[T]): The expected format of the research results,
                extracted per site.
            run_id (Optional[str]): If you want to retry a workflow run, this is the
                ID of an existing run to respawn.
            extra_instructions (Optional[List[ChatCompletionMessageParam]]):
                Additional instruction messages to prepend to the prompt.

        Returns:
            WorkflowRunHandle[AllResearchResults[T]]: Handle for the spawned workflow run.
        """
        return webresearch_scrape(
            self._config.http_client,
            self._config.core,
            CreateScrapeRequest(
                workflow_id=workflow_id,
                run_id=run_id,
                site=Url(site),
                research_schema=research_schema.model_json_schema(),
                extra_instructions=extra_instructions,
            ),
            research_schema,
        )
