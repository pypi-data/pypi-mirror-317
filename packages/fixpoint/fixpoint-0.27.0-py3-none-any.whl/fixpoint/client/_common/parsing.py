"""Common functions for parsing operations."""

__all__ = [
    "create_webpage_parse",
    "async_create_webpage_parse",
    "create_crawl_parse",
    "async_create_crawl_parse",
    "create_batch_webpage_parse",
    "async_create_batch_webpage_parse",
]

import httpx

from fixpoint_common.types.parsing import (
    CreateWebpageParseRequest,
    WebpageParseResult,
    CreateCrawlUrlParseRequest,
    CrawlUrlParseResult,
    CreateBatchWebpageParseRequest,
    BatchWebpageParseResult,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig

_PARSE_ROUTE = "/parses"
_WEB_PARSE_ROUTE = f"{_PARSE_ROUTE}/webpage_parses"
_CRAWL_PARSE_ROUTE = f"{_PARSE_ROUTE}/crawl_url_parses"
_BATCH_WEB_PARSE_ROUTE = f"{_PARSE_ROUTE}/batch_webpage_parses"


def create_webpage_parse(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateWebpageParseRequest,
) -> WebpageParseResult:
    """Create a webpage parse request synchronously."""
    resp = http_client.post(config.route_url(_WEB_PARSE_ROUTE), json=req.model_dump())
    return _process_webpage_parse_response(resp)


async def async_create_webpage_parse(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateWebpageParseRequest,
) -> WebpageParseResult:
    """Create a webpage parse request asynchronously."""
    resp = await http_client.post(
        config.route_url(_WEB_PARSE_ROUTE), json=req.model_dump()
    )
    return _process_webpage_parse_response(resp)


def _process_webpage_parse_response(resp: httpx.Response) -> WebpageParseResult:
    raise_for_status(resp)
    return WebpageParseResult.model_validate(resp.json())


def create_crawl_parse(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateCrawlUrlParseRequest,
) -> CrawlUrlParseResult:
    """Create a crawl parse request synchronously."""
    resp = http_client.post(config.route_url(_CRAWL_PARSE_ROUTE), json=req.model_dump())
    return _process_crawl_parse_response(resp)


async def async_create_crawl_parse(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateCrawlUrlParseRequest,
) -> CrawlUrlParseResult:
    """Create a crawl parse request asynchronously."""
    resp = await http_client.post(
        config.route_url(_CRAWL_PARSE_ROUTE), json=req.model_dump()
    )
    return _process_crawl_parse_response(resp)


def _process_crawl_parse_response(resp: httpx.Response) -> CrawlUrlParseResult:
    raise_for_status(resp)
    return CrawlUrlParseResult.model_validate(resp.json())


def create_batch_webpage_parse(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateBatchWebpageParseRequest,
) -> BatchWebpageParseResult:
    """Create a batch webpage parse request synchronously."""
    resp = http_client.post(
        config.route_url(_BATCH_WEB_PARSE_ROUTE), json=req.model_dump()
    )
    return _process_batch_webpage_parse_response(resp)


async def async_create_batch_webpage_parse(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateBatchWebpageParseRequest,
) -> BatchWebpageParseResult:
    """Create a crawl parse request asynchronously."""
    resp = await http_client.post(
        config.route_url(_BATCH_WEB_PARSE_ROUTE), json=req.model_dump()
    )
    return _process_batch_webpage_parse_response(resp)


def _process_batch_webpage_parse_response(
    resp: httpx.Response,
) -> BatchWebpageParseResult:
    raise_for_status(resp)
    return BatchWebpageParseResult.model_validate(resp.json())
