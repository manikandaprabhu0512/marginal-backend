import asyncio

from flows.chat_flow import run_chat
from graph.consume_graph import consume_graph
from helper.event_bus import EventType, event_bus
from helper.sse_event import sse_event


async def event_stream(conversation_id: str, query: str):
    print("Event Stream Called...")

    graph_task = asyncio.create_task(
        consume_graph(conversation_id, query)
    )

    async for event in event_bus.subscribe(conversation_id):

        yield sse_event(
            event.type.value,
            event.data,
        )

        if event.type == EventType.INGESTION_COMPLETED:
            break

    await graph_task

    async for item in run_chat(conversation_id,query,[],False):
        yield item