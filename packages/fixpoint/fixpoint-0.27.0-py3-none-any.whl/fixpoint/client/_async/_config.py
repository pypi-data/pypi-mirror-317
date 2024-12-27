"""Configuration and extra clients for the async Fixpoint API client."""

__all__ = ["AsyncConfig"]

from dataclasses import dataclass

from httpx import AsyncClient

from .._common import ApiCoreConfig


@dataclass
class AsyncConfig:
    """Configuration and extra clients for the async Fixpoint API client."""

    core: ApiCoreConfig
    http_client: AsyncClient

    def route_url(self, route: str) -> str:
        """Join the base URL with the given route."""
        return self.core.route_url(route)
