import time

from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.worker_state import WorkerState, WorkerStatus
from helper.process_page import process_page
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def page_vectorizer_node(state: WorkerState):

    with tracer.start_as_current_span("Page Vectorizer") as span:

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
                    "process_time": round(time.perf_counter() - state["start_time"], 2),
                }                
            }