import json

from agents.sources_summary_agent import get_sources_summary_agent
from db.crud import save_turn
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.json_parser import parse_agent_json
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def source_summary_node(state: GraphState):

    with tracer.start_as_current_span("Source Summary"):
        source_summarizer = get_sources_summary_agent()

        source_summary = await retry_async(
            lambda: source_summarizer.ainvoke({"messages": [{"role": "user", "content": json.dumps({"sources": state["titles"]})}]})
        )

        source_summary_data = parse_agent_json(source_summary["messages"][-1].content)

        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=IngestionEventType.SUMMARY_READY,
                data={
                    "summary": source_summary_data["summary"],
                },
            )
        )

        await retry_async(
            lambda: save_turn(
                conversation_id=state["conversation_id"],
                user_id=state["user_id"],
                events=state["events"],
                assistant={
                    "answer": source_summary_data["summary"],
                },
            )
        )

        return {}