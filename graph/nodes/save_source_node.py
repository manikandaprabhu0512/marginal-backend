from db.crud import save_sources
from graph.state import GraphState
from helper.file_type import detect_source_type
from helper.retry import retry_async


async def save_source_node(state: GraphState):
    sources = []

    for result in state["page_results"]:

        if isinstance(result, Exception):
            print(f"Page processing failed: {result}")
            continue

        if not result["title"] or not result["url"]:
            continue

        sources.append(
            {"title": result["title"],"url": result["url"],"source_type": detect_source_type(result["url"]),"vector_ids": result.get("vector_ids", [])}
        )

    if sources:
        await retry_async(
            lambda: save_sources(
                state["conversation_id"],
                sources,
            )
        )
        
    return {}