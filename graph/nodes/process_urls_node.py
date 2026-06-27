import asyncio

from graph.process_url_graph import process_url_graph
from graph.state import GraphState


async def process_urls_node(state: GraphState):

    for url in state["url_list"]:
        await process_url_graph.ainvoke({"conversation_id": state["conversation_id"],"url": url})

    return {}