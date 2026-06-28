from graph.ingestion_graph.worker_state import WorkerState, WorkerStatus
from helper.process_page import process_page
from helper.retry import retry_async


async def page_vectorizer_node(state: WorkerState):

    if state["status"] == WorkerStatus.FAILED:
        return {}

    try:
        page_result = await retry_async(
            lambda: process_page(state["page"],state["conversation_id"])
        )

        return {
            "page_result": page_result,
        }

    except Exception as e:

        return {
            "status": WorkerStatus.FAILED,
            "error": str(e),
        }