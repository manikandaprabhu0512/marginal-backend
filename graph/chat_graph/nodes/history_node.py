from db.crud import get_history
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.retry import retry_async


async def history_node(state: ChatState):

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.FETCHING_HISTORY,
            data={},
        )
    )

    history = await retry_async(
        lambda: get_history(state["conversation_id"])
    )

    return {
        "history": history,
    }