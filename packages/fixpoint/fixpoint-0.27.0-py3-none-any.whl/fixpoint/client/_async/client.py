"""Async client for interacting with the Fixpoint API"""

__all__ = ["AsyncFixpointClient"]

from typing import Optional

import httpx

from fixpoint_common.constants import DEFAULT_API_CLIENT_TIMEOUT
from fixpoint_common.utils.http import new_api_key_http_header
from .._common import ApiCoreConfig, ApiVersion
from ._config import AsyncConfig
from .agents import AsyncAgents
from .human import AsyncHuman
from .documents import AsyncDocuments
from .research import AsyncResearch
from .workflows import AsyncWorkflows
from .extractions import AsyncExtractions
from .parsing import AsyncParsing
from .sitemaps import AsyncSitemaps


class V0AsyncFixpointClient:
    """Old APIs that are deprecated"""

    _config: AsyncConfig
    agents: AsyncAgents
    human: AsyncHuman
    documents: AsyncDocuments

    def __init__(self, config: AsyncConfig):
        self._config = config
        self.agents = AsyncAgents(self._config)
        self.human = AsyncHuman(self._config)
        self.documents = AsyncDocuments(self._config)

    @property
    def docs(self) -> AsyncDocuments:
        """Async interface for interacting with documents."""
        return self.documents


class AsyncFixpointClient:
    """Async client for interacting with the Fixpoint API"""

    _config: AsyncConfig
    workflows: AsyncWorkflows
    research: AsyncResearch
    extractions: AsyncExtractions
    parses: AsyncParsing
    sitemaps: AsyncSitemaps

    v0: V0AsyncFixpointClient
    """Old APIs that are deprecated"""

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        *,
        api_version: ApiVersion = "v1",
        timeout: float = DEFAULT_API_CLIENT_TIMEOUT,
        _transport: Optional[httpx.ASGITransport] = None,
        _sync_transport: Optional[httpx.WSGITransport] = None,
    ):
        http_client = httpx.AsyncClient(
            transport=_transport,
            timeout=timeout,
            headers=new_api_key_http_header(api_key),
        )
        # Some of the internal code instantiates a sync HTTP client, even though
        # our code here is primarily sync. In such a case, we'd prefer to be
        # able to still override the transport when we need to, such as for
        # testing. So declare an sync HTTP client here, even though we won't use
        # it for the most part.
        sync_http_client = httpx.Client(
            transport=_sync_transport,
            timeout=timeout,
            headers=new_api_key_http_header(api_key),
        )
        core_config = ApiCoreConfig.from_api_info(
            api_key=api_key,
            api_url=api_url,
            http_client=sync_http_client,
            ahttp_client=http_client,
            api_version=api_version,
        )
        self._config = AsyncConfig(core_config, http_client)
        self.workflows = AsyncWorkflows(self._config)
        self.research = AsyncResearch(self._config)
        self.extractions = AsyncExtractions(self._config)
        self.parses = AsyncParsing(self._config)
        self.sitemaps = AsyncSitemaps(self._config)
        self.v0 = V0AsyncFixpointClient(self._config)
