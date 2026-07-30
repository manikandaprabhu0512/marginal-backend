import time

from db.crud import save_source
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.worker_state import WorkerState, WorkerStatus
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def save_source_node(state: WorkerState):

    with tracer.start_as_current_span("Save source"):
        if state["status"] == WorkerStatus.FAILED:
            return {}

        try:

            await retry_async(
                lambda: save_source(conversation_id=state["conversation_id"],source=state["page_result"])
            )

            await event_bus.publish(
                Event(
                    conversation_id=state["conversation_id"],
                    type=IngestionEventType.PAGE_LOADING_COMPLETED,
                    data={
                        "url": state["url"],
                        "process_time": round(time.perf_counter() - state["started_at"], 2),
                    },
                )
            )

            return {
                "status": WorkerStatus.SUCCESS,
            }

        except Exception as e:

            return {
                "status": WorkerStatus.FAILED,
                "error": str(e),
            }