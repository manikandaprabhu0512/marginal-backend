import asyncio

from graph.state import GraphState
from helper.event_bus import Event, EventType, event_bus
from helper.load_page import load_page


async def load_page_node(state: GraphState):
    loaded_pages = await asyncio.gather(
        *[load_page(url) for url in state["url_list"]],
        return_exceptions=False,
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