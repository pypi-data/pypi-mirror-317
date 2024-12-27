"""
Synchronous interface for sitemaps
"""

__all__ = ["Sitemaps"]

from fixpoint_common.types.sitemap import (
    CreateSitemapRequest,
    Sitemap,
)
from .._common.sitemaps import create_sitemap
from ._config import Config


class Sitemaps:
    """Synchronous interface for sitemaps."""

    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, req: CreateSitemapRequest) -> Sitemap:
        """Create a sitemap.

        Args:
            req (CreateSitemapRequest): The request to create a sitemap.

        Returns:
            Sitemap: The created sitemap.

        Raises:
            FixpointApiError: If there's an error in the API HTTP request.
        """
        return create_sitemap(
            self._config.http_client,
            self._config.core,
            req,
        )
