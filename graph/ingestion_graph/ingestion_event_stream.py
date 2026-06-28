import asyncio

from graph.chat_graph.chat_event_stream import chat_event_stream
from graph.event_bus import event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.consume_graph import consume_graph
from helper.sse_event import sse_event


async def ingestion_event_stream(conversation_id: str, query: str):

    graph_task = asyncio.create_task(
        consume_graph(conversation_id, query)
    )

    async for event in event_bus.subscribe(conversation_id):

        yield sse_event(
            event.type.value,
            event.data,
        )

        if event.type == IngestionEventType.INGESTION_COMPLETED:
            break

    await graph_task

    async for item in chat_event_stream(
        conversation_id=conversation_id,
        message=query,
        excluded_urls=[],
        skip_save_user=False,
    ):
        yield item