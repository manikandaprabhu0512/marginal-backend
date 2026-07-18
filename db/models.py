from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Conversation(Document):
    conversation_id: str
    title: str = "Untitled Notebook"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_count: int = 0

    class Settings:
        name = "conversations"


class Message(Document):
    conversation_id: str
    role: str
    content: str
    file_url: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"


class Source(Document):
    conversation_id: str
    url: str
    title: str
    source_type: str = "link"   # "link" | "pdf" | "text" | "document" | "video"
    vector_ids: list[str] = Field(default_factory=list)

    class Settings:
        name = "sources"

class ScrapedURLs(Document):
    conversation_id: str
    query: str
    url_list: list[dict] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "scraped_urls"
        indexes = [
            [("conversation_id", 1), ("query", 1)]
        ]
