"""Common code for the Web Researcher agent."""

__all__ = [
    "webresearch_scrape",
    "async_webresearch_scrape",
]

from typing import Type, TypeVar

import httpx
from httpx import Client, AsyncClient
from pydantic import BaseModel

from fixpoint_common.webresearcher import (
    AllResearchResultsPydantic as AllResearchResults,
    CreateScrapeRequest,
    ScrapeResult,
    convert_api_to_pydantic,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig


BM = TypeVar("BM", bound=BaseModel)


_SCRAPE_ROUTE = "/agents/webresearcher/scrapes"


def webresearch_scrape(
    http_client: Client,
    config: ApiCoreConfig,
    req: CreateScrapeRequest,
    pydantic_schema: Type[BM],
) -> AllResearchResults[BM]:
    """Make a synchronous web research scrape request"""
    resp = http_client.post(
        config.route_url(_SCRAPE_ROUTE),
        json=req.model_dump(),
    )
    # only raises if we got an error response
    return _process_resp(resp, pydantic_schema)


async def async_webresearch_scrape(
    http_client: AsyncClient,
    config: ApiCoreConfig,
    req: CreateScrapeRequest,
    pydantic_schema: Type[BM],
) -> AllResearchResults[BM]:
    """Make an asynchronous web research scrape request"""
    resp = await http_client.post(
        config.route_url(_SCRAPE_ROUTE),
        json=req.model_dump(),
    )
    return _process_resp(resp, pydantic_schema)


def _process_resp(
    resp: httpx.Response, pydantic_schema: Type[BM]
) -> AllResearchResults[BM]:
    # only raises if we got an error response
    raise_for_status(resp)
    result = ScrapeResult.model_validate(resp.json())
    return convert_api_to_pydantic(pydantic_schema, result)
