"""Types for the Fixpoint client and its APIs."""

__all__ = [
    "AllResearchResultsPydantic",
    "BatchExtractionJob",
    "BatchExtractionJobStatus",
    "BatchTextSource",
    "BatchWebpageParseResult",
    "BatchWebpageSource",
    "Citation",
    "CrawlUrlParseResult",
    "CrawlUrlSource",
    "CreateBatchExtractionJobRequest",
    "CreateBatchWebpageParseRequest",
    "CreateCrawlUrlParseRequest",
    "CreateHumanTaskEntryRequest",
    "CreateJsonSchemaExtractionRequest",
    "CreateRecordExtractionRequest",
    "CreateResearchRecordRequest",
    "CreateSitemapRequest",
    "CreateWebpageParseRequest",
    "Document",
    "HumanTaskEntry",
    "JsonSchemaExtraction",
    "ListDocumentsResponse",
    "ListHumanTaskEntriesResponse",
    "ListResearchRecordsResponse",
    "NodeStatus",
    "RecordExtraction",
    "ResearchField",
    "ResearchFieldEditableConfig",
    "ResearchRecord",
    "Sitemap",
    "Source",
    "TaskEntryField",
    "TaskFieldEditableConfig",
    "TextCitation",
    "TextSource",
    "WebPageCitation",
    "WebpageParseResult",
    "WebpageSource",
]

from fixpoint_common.types import Document, ListDocumentsResponse, NodeStatus
from fixpoint_common.types.human import (
    HumanTaskEntry,
    CreateHumanTaskEntryRequest,
    EntryField as TaskEntryField,
    EditableConfig as TaskFieldEditableConfig,
    ListHumanTaskEntriesResponse,
)
from fixpoint_common.types.research import (
    ResearchRecord,
    ResearchField,
    CreateResearchRecordRequest,
    ListResearchRecordsResponse,
    EditableConfig as ResearchFieldEditableConfig,
)
from fixpoint_common.webresearcher.types import AllResearchResultsPydantic
from fixpoint_common.types.extraction import (
    CreateRecordExtractionRequest,
    RecordExtraction,
    CreateBatchExtractionJobRequest,
    BatchExtractionJob,
    BatchExtractionJobStatus,
)
from fixpoint_common.types.json_extraction import (
    CreateJsonSchemaExtractionRequest,
    JsonSchemaExtraction,
)
from fixpoint_common.types.parsing import (
    BatchWebpageParseResult,
    CrawlUrlParseResult,
    CreateBatchWebpageParseRequest,
    CreateCrawlUrlParseRequest,
    CreateWebpageParseRequest,
    WebpageParseResult,
)
from fixpoint_common.types.sources import (
    BatchTextSource,
    BatchWebpageSource,
    CrawlUrlSource,
    Source,
    TextSource,
    WebpageSource,
)
from fixpoint_common.types.citations import Citation, TextCitation, WebPageCitation
from fixpoint_common.types.sitemap import CreateSitemapRequest, Sitemap
