"""Configuration and extra clients for the sync Fixpoint API client."""

__all__ = ["Config"]

from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import Client

from .._common import ApiCoreConfig


@dataclass
class Config:
    """Configuration and extra clients for the sync Fixpoint API client."""

    core: ApiCoreConfig
    http_client: Client

    def route_url(self, route: str) -> str:
        """Join the base URL with the given route."""
        return urljoin(self.core.api_url, route)
