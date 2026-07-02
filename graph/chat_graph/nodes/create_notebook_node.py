from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType


async def create_notebook_node(state: ChatState):
    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.CREATED_NOTEBOOK,
            data={},
        )
    )

    return {}