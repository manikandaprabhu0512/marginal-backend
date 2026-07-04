from graph.chat_graph.chat_state import ChatState
from graph.ingestion_graph.add_source_graph import add_sources_graph


async def add_sources_node(state: ChatState):
    ingestion_state = {
        "conversation_id": state["conversation_id"],
        "query": state["message"],
        "rewritten_query": state["rewritten_query"],
        "url_list" : None
    }

    await add_sources_graph.ainvoke(ingestion_state)

    return {}