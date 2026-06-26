import asyncio

from graph.state import GraphState
from helper.event_bus import Event, EventType, event_bus
from helper.process_page import process_page
from helper.retry_failed_items import retry_failed_items


async def page_vectorizer_node(state: GraphState):
    page_results = await retry_failed_items(
        items=state["pages"],
        processor=lambda page: process_page(
            page,
            state["conversation_id"],
        ),
    )

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=EventType.PAGE_VECTORIZED,
            data={},
        )
    )

    return {
        "page_results": page_results,
    }