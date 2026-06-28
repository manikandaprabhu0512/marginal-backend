from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.retry import retry_async
from tools.retriever_tool import retrieve_context


async def retrieve_context_node(state: ChatState):

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.RETRIEVING_CONTEXT,
            data={},
        )
    )

    context = await retry_async(
        lambda: retrieve_context(state["conversation_id"], state["message"], state["excluded_urls"])
    )

    return {
        "context": context,
    }