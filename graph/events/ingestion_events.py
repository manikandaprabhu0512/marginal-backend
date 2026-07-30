from enum import Enum


class IngestionEventType(str, Enum):
    QUERY_REWRITTEN = "query_rewritten"
    TITLE_GENERATED = "title_generated"
    SEARCH_STARTED = "search_started"
    SEARCH_COMPLETED = "search_completed"
    SOURCE_LOADED = "source_loaded"
    PAGE_LOADING_STARTED = "page_loading_started"
    PAGE_LOADING_COMPLETED = "page_loading_completed"
    INGESTION_COMPLETED = "ingestion_completed"
    SUMMARY_READY= "summary_ready"
    ERROR = "error"