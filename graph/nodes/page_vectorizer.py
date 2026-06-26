import asyncio

from graph.state import GraphState
from helper.event_bus import Event, EventType, event_bus
from helper.process_page import process_page


async def page_vectorizer_node(state: GraphState):
    page_results = await asyncio.gather(
        *[
            process_page(page, state["conversation_id"])
            for page in state["pages"]
        ],
        return_exceptions=True,
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