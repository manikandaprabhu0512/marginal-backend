import asyncio

from background.cleanup import cleanup_ingestion
from background.manager import background_manager
from graph.ingestion_graph.process_url_graph import process_url_graph
from graph.ingestion_graph.state import GraphState
from graph.ingestion_graph.worker_state import WorkerStatus


async def process_urls_node(state: GraphState):

    await asyncio.gather(
        *[
            process_url_graph.ainvoke(
                {
                    "conversation_id": state["conversation_id"],
                    "url": url,
                    "status": WorkerStatus.PENDING,
                    "error": None,
                    "page": None,
                    "page_result": None,
                }
            )
            for url in state["url_list"]
        ],
        return_exceptions=True,
    )

    background_manager.submit(
        cleanup_ingestion(state["conversation_id"],state["query"])
    )
    print("deleted from db...")

    return {}