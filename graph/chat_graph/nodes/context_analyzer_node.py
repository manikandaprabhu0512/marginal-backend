from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType


async def context_analyzer(state: ChatState):
    context = state["context"]

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.ANALYZING_CONTEXT,
            data={},
        )
    )


    if not context.strip():
        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.INSUFFICIENT_CONTEXT,
                data={},
            )
        )

        return {"insufficient": True}
    
    return {"insufficient": False}