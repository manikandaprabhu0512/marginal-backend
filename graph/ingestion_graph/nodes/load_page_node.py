import time

from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.worker_state import WorkerState, WorkerStatus
from helper.load_page import load_page
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def load_page_node(state: WorkerState):
    with tracer.start_as_current_span("Page load"):
        try:
            print("Page Loading...")
            start_time = time.perf_counter()
            await event_bus.publish(
                Event(
                    conversation_id=state["conversation_id"],
                    type=IngestionEventType.PAGE_LOADING_STARTED,
                    data={
                        "url": state["url"],
                    },
                )
            )

            page = await retry_async(
                lambda: load_page(
                    state["url"]
                )
            )

            return {
                "page": page,
                "status": WorkerStatus.SUCCESS,
                "started_at" : start_time
            }

        except Exception as e:

            await event_bus.publish(
                Event(
                    conversation_id=state["conversation_id"],
                    type=IngestionEventType.PAGE_LOADING_FAILED,
                    data={
                        "url": state["url"],
                    },
                )
            )

            return {
                "status": WorkerStatus.FAILED,
                "error": str(e),
                "events": {
                    "status": "failed",
                    "url": state["url"],
                    "process_time": round(time.perf_counter() - start_time, 2),
                }
            }