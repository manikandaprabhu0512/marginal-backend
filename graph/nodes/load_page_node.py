import asyncio

from graph.state import GraphState
from helper.event_bus import Event, EventType, event_bus
from helper.load_page import load_page
from helper.retry_failed_items import retry_failed_items


async def load_page_node(state: GraphState):
    loaded_pages = await retry_failed_items(
        items=state["url_list"],
        processor=load_page,
    )

    pages = [page for page in loaded_pages if page is not None]
    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=EventType.PAGE_LOADED,
            data={
                "pages_loaded": len(pages),
            },
        )
    )

    return {
        "pages": pages,
    }