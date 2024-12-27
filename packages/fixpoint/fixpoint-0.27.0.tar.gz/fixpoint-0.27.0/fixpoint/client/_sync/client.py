"""Client for interacting with the Fixpoint API"""

__all__ = ["FixpointClient"]

from typing import Optional

import httpx

from fixpoint_common.constants import DEFAULT_API_CLIENT_TIMEOUT
from fixpoint_common.utils.http import new_api_key_http_header
from .._common import ApiCoreConfig, ApiVersion
from ._config import Config
from .agents import Agents
from .human import Human
from .documents import Documents
from .research import Research
from .extractions import Extractions
from .parsing import Parsing
from .sitemaps import Sitemaps


class V0FixpointClient:
    """Old APIs that are deprecated"""

    _config: Config
    agents: Agents
    human: Human
    documents: Documents

    def __init__(self, config: Config):
        self._config = config
        self.agents = Agents(self._config)
        self.human = Human(self._config)
        self.documents = Documents(self._config)

    @property
    def docs(self) -> Documents:
        """Interface to documents."""
        return self.documents


class FixpointClient:
    """Client for interacting with the Fixpoint API"""

    _config: Config
    research: Research
    extractions: Extractions
    parses: Parsing
    sitemaps: Sitemaps

    v0: V0FixpointClient
    """Old APIs that are deprecated"""

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        *,
        api_version: ApiVersion = "v1",
        timeout: float = DEFAULT_API_CLIENT_TIMEOUT,
        _transport: Optional[httpx.WSGITransport] = None,
        _async_transport: Optional[httpx.ASGITransport] = None,
    ):
        http_client = httpx.Client(
            transport=_transport,
            timeout=timeout,
            headers=new_api_key_http_header(api_key),
        )
        # Some of the internal code instantiates an async HTTP client, even
        # though our code here is primarily async. In such a case, we'd prefer
        # to be able to still override the transport when we need to, such as
        # for testing. So declare an async HTTP client here, even though we
        # won't use it for the most part.
        async_http_client = httpx.AsyncClient(
            transport=_async_transport,
            timeout=timeout,
            headers=new_api_key_http_header(api_key),
        )
        core_config = ApiCoreConfig.from_api_info(
            api_key=api_key,
            api_url=api_url,
            http_client=http_client,
            ahttp_client=async_http_client,
            api_version=api_version,
        )
        self._config = Config(core_config, http_client)
        self.research = Research(self._config)
        self.extractions = Extractions(self._config)
        self.parses = Parsing(self._config)
        self.sitemaps = Sitemaps(self._config)
        self.v0 = V0FixpointClient(self._config)
