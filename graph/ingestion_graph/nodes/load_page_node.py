from graph.ingestion_graph.worker_state import WorkerState, WorkerStatus
from helper.load_page import load_page
from helper.retry import retry_async


async def load_page_node(state: WorkerState):
    try:
        page = await retry_async(
            lambda: load_page(
                state["url"]
            )
        )

        return {
            "page": page,
            "status": WorkerStatus.SUCCESS,
        }

    except Exception as e:

        return {
            "status": WorkerStatus.FAILED,
            "error": str(e),
        }