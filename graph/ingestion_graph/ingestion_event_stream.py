import asyncio
import time

from graph.chat_graph.chat_event_stream import chat_event_stream
from graph.event_bus import event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.consume_graph import consume_graph
from helper.sse_event import sse_event
from telemetry.instrumentation import tracer
from telemetry.metrics import ingestion_duration


async def ingestion_event_stream(conversation_id: str, query: str):

    start = time.perf_counter()

    try:
        with tracer.start_as_current_span("Ingestion"):
            graph_task = asyncio.create_task(
                consume_graph(conversation_id, query)
            )

            async for event in event_bus.subscribe(conversation_id):

                yield sse_event(
                    event.type.value,
                    event.data,
                )

                if event.type == IngestionEventType.SUMMARY_READY:
                    break

            await graph_task

            yield sse_event(
                "done",
                {},
            )
    
    finally:
        ingestion_duration.record(
            time.perf_counter() - start
        )