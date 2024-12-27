"""
Asynchronous interface for sitemaps
"""

__all__ = ["AsyncSitemaps"]

from fixpoint_common.types.sitemap import (
    CreateSitemapRequest,
    Sitemap,
)
from .._common.sitemaps import async_create_sitemap
from ._config import AsyncConfig


class AsyncSitemaps:
    """Asynchronous interface for sitemaps."""

    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(self, req: CreateSitemapRequest) -> Sitemap:
        """Create a sitemap.

        Args:
            req (CreateSitemapRequest): The request to create a sitemap.

        Returns:
            Sitemap: The created sitemap.

        Raises:
            FixpointApiError: If there's an error in the API HTTP request.
        """
        return await async_create_sitemap(
            self._config.http_client,
            self._config.core,
            req,
        )
