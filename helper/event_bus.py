import asyncio
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EventType(str, Enum):
    TITLE_GENERATED = "title_generated"
    SEARCH_STARTED = "search_started"
    SEARCH_COMPLETED = "search_completed"
    PAGE_LOADED = "page_loaded"
    PAGE_SUMMARIZED = "page_summarized"
    PAGE_VECTORIZED = "page_vectorized"
    INGESTION_COMPLETED = "ingestion_completed"
    ERROR = "error"


class Event(BaseModel):
    conversation_id: str

    type: EventType

    data: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class EventBus:

    def __init__(self):
        self._queues: dict[str, asyncio.Queue[Event]] = {}

    def _get_queue(self, conversation_id: str) -> asyncio.Queue[Event]:
        if conversation_id not in self._queues:
            self._queues[conversation_id] = asyncio.Queue()

        return self._queues[conversation_id]

    async def publish(self, event: Event):
        print(f"Publishing event: {event.data}")
        queue = self._get_queue(event.conversation_id)
        await queue.put(event)

    async def subscribe(self, conversation_id: str):
        queue = self._get_queue(conversation_id)

        while True:
            yield await queue.get()

    def cleanup(self, conversation_id: str):
        self._queues.pop(conversation_id, None)


event_bus = EventBus()