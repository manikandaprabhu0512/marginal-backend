from enum import Enum


class IngestionEventType(str, Enum):
    QUERY_REWRITTEN = "query_rewritten"
    TITLE_GENERATED = "title_generated"
    SEARCH_STARTED = "search_started"
    SEARCH_COMPLETED = "search_completed"
    SOURCE_LOADED = "source_loaded"
    INGESTION_COMPLETED = "ingestion_completed"
    ERROR = "error"