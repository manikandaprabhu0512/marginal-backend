from config.redis_config import redis_config
from graph.chat_graph.chat_state import ChatState
from graph.chat_graph.nodes.history_node import history_node


async def context_conformation_node(state: ChatState):

    print("Calling Context Conformation Node....")

    history = state.get("history")
    context = state.get("context")

    if not history:
        print("Histroy Fetching...")
        history = await history_node(state)
        print("History Fetched: ", history)
    if not context:
        print("Context Fetching...")
        context = redis_config.get(state["conversation_id"])
        if context:
            context = context.decode("utf-8")
        print("Context Fetched: ", len(context))
        print("Context Fetched...")

    print("Existing History Fetched: ", history)
    print("Existing Context Fetched: ", len(context))
    print("Moving to Smaller Model...")

    return {
        "history": history,
        "context": context,
    }