import json

from agents.ingestion_query_rewriter_agent import get_ingestion_query_rewriter
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.json_parser import parse_agent_json
from telemetry.instrumentation import tracer


async def ingestion_query_rewriter_node(state: GraphState):
    with tracer.start_as_current_span("Ingestion Query Rewriter"):
    
        rewriter = get_ingestion_query_rewriter()

        with tracer.start_as_current_span("Generating rewritten query") as rewrite_span:
            rewrite_result = await rewriter.ainvoke({
                "messages": [{"role": "user", "content": json.dumps({"query": state["query"]})}]
            })

        with tracer.start_as_current_span("Parsing rewritten query"):
            rewrite_data = parse_agent_json(rewrite_result["messages"][-1].content)
    
            rewritten_query = rewrite_data.get("rewritten_query") or state["query"]

            rewrite_span.set_attribute("rewritten_query", rewritten_query)

            await event_bus.publish(
                Event(
                    conversation_id=state["conversation_id"],
                    type=IngestionEventType.QUERY_REWRITTEN,
                    data={
                        "rewritten_query": rewritten_query,
                    },
                )
            )

            return {
                "rewritten_query" : rewritten_query
            }