"""
Asynchronous interface for parsing webpages and crawling URLs.
"""

__all__ = ["AsyncParsing"]

from fixpoint_common.types.parsing import (
    CreateWebpageParseRequest,
    WebpageParseResult,
    CreateCrawlUrlParseRequest,
    CrawlUrlParseResult,
    CreateBatchWebpageParseRequest,
    BatchWebpageParseResult,
)
from .._common.parsing import (
    async_create_webpage_parse,
    async_create_crawl_parse,
    async_create_batch_webpage_parse,
)
from ._config import AsyncConfig


class _AsyncWebpageParsing:
    """Asynchronous interface for webpage parsing."""

    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(self, req: CreateWebpageParseRequest) -> WebpageParseResult:
        """Parse a single webpage.

        Args:
            req (CreateWebpageParseRequest): The request containing details for the
                webpage parse.

        Returns:
            WebpageParseResult: The parsed webpage content.

        Raises:
            HTTPException: If there's an error in the HTTP request.
        """
        return await async_create_webpage_parse(
            self._config.http_client,
            self._config.core,
            req,
        )

    async def create_batch(
        self, req: CreateBatchWebpageParseRequest
    ) -> BatchWebpageParseResult:
        """Parse a batch of webpages.

        Args:
            req (CreateBatchWebpageParseRequest): The request containing details for the
                batch webpage parse.

        Returns:
            BatchWebpageParseResult: The parsed webpage content.

        Raises:
            FixpointApiError: If there's an error in the API HTTP request.
        """
        return await async_create_batch_webpage_parse(
            self._config.http_client,
            self._config.core,
            req,
        )


class _AsyncCrawlParsing:
    """Asynchronous interface for crawl parsing."""

    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(self, req: CreateCrawlUrlParseRequest) -> CrawlUrlParseResult:
        """Parse multiple webpages by crawling from a starting URL.

        Args:
            req (CreateCrawlUrlParseRequest): The request containing details for the
                crawl parse.

        Returns:
            CrawlUrlParseResult: The parsed contents from crawled pages.

        Raises:
            HTTPException: If there's an error in the HTTP request.
        """
        return await async_create_crawl_parse(
            self._config.http_client,
            self._config.core,
            req,
        )


class AsyncParsing:
    """Asynchronous interface for webpage and crawl parsing."""

    _config: AsyncConfig
    webpage: _AsyncWebpageParsing
    crawl: _AsyncCrawlParsing

    def __init__(self, config: AsyncConfig):
        self._config = config
        self.webpage = _AsyncWebpageParsing(config)
        self.crawl = _AsyncCrawlParsing(config)
