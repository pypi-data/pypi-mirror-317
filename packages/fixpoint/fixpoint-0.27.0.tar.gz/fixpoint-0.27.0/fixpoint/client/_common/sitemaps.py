"""Common functions for sitemap operations."""

__all__ = [
    "create_sitemap",
    "async_create_sitemap",
]

import httpx

from fixpoint_common.types.sitemap import (
    CreateSitemapRequest,
    Sitemap,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig

_BASE_SITEMAPS_ROUTE = "/sitemaps"
_CREATE_ROUTE = f"{_BASE_SITEMAPS_ROUTE}"


def create_sitemap(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateSitemapRequest,
) -> Sitemap:
    """Create a sitemap synchronously."""
    resp = http_client.post(config.route_url(_CREATE_ROUTE), json=req.model_dump())
    return _process_create_sitemap_response(resp)


async def async_create_sitemap(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateSitemapRequest,
) -> Sitemap:
    """Create a webpage parse request asynchronously."""
    resp = await http_client.post(
        config.route_url(_CREATE_ROUTE), json=req.model_dump()
    )
    return _process_create_sitemap_response(resp)


def _process_create_sitemap_response(resp: httpx.Response) -> Sitemap:
    raise_for_status(resp)
    return Sitemap.model_validate(resp.json())
