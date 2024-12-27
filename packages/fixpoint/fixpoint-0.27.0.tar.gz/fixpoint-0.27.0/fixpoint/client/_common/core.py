"""Common code for sync and async Fixpoint clients."""

__all__ = ["ApiCoreConfig", "ApiVersion"]

from dataclasses import dataclass
from typing import Literal, Optional, TypeVar

import httpx
from pydantic import BaseModel

from fixpoint_common.config import get_env_api_url
from fixpoint_common.utils.http import route_url
from fixpoint_common.workflows.structured import RunConfig
from fixpoint_common.workflows.imperative import StorageConfig


BM = TypeVar("BM", bound=BaseModel)

ApiVersion = Literal["v1", "latest"]


@dataclass
class ApiCoreConfig:
    """Configuration for the Fixpoint API"""

    api_key: str
    api_url: str
    run_config: RunConfig
    storage_config: StorageConfig
    api_version: ApiVersion = "v1"

    @classmethod
    def from_api_info(
        cls,
        api_key: str,
        api_url: Optional[str] = None,
        api_version: ApiVersion = "v1",
        http_client: Optional[httpx.Client] = None,
        ahttp_client: Optional[httpx.AsyncClient] = None,
    ) -> "ApiCoreConfig":
        """Create an ApiConfig from an API key and API URL"""
        if api_url is None:
            api_url = get_env_api_url()
        run_config = RunConfig.with_api(
            api_key=api_key,
            api_url=api_url,
            http_client=http_client,
            ahttp_client=ahttp_client,
        )
        storage_config = run_config.storage
        return cls(api_key, api_url, run_config, storage_config, api_version)

    def route_url(self, *route_parts: str) -> str:
        """Join the base URL with the given route."""
        if self.api_version == "latest":
            return route_url(self.api_url, *route_parts)
        return route_url(self.api_url, self.api_version, *route_parts)
