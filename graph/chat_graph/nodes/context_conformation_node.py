from config.redis_config import redis_config
from graph.chat_graph.chat_state import ChatState
from graph.chat_graph.nodes.history_node import history_node


async def context_conformation_node(state: ChatState):

    history = state.get("history")
    context = state.get("context")

    if not history:
        history = await history_node(state)
    if not context:
        context = redis_config.get(state["conversation_id"])
        if context:
            context = context.decode("utf-8")

    return {
        "history": history,
        "context": context,
    }