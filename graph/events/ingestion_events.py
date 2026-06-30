from enum import Enum


class IngestionEventType(str, Enum):
    QUERY_REWRITTEN = "query_rewritten"
    TITLE_GENERATED = "title_generated"
    SEARCH_STARTED = "search_started"
    SEARCH_COMPLETED = "search_completed"
    PAGE_LOADED = "page_loaded"
    PAGE_SUMMARIZED = "page_summarized"
    PAGE_VECTORIZED = "page_vectorized"
    INGESTION_COMPLETED = "ingestion_completed"
    ERROR = "error"