import json

from agents.ingestion_query_rewriter_agent import get_ingestion_query_rewriter
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.json_parser import parse_agent_json


async def ingestion_query_rewriter_node(state: GraphState):
    rewriter = get_ingestion_query_rewriter()
    rewrite_result = await rewriter.ainvoke({
        "messages": [{"role": "user", "content": json.dumps({"query": state["query"]})}]
    })
    rewrite_data = parse_agent_json(rewrite_result["messages"][-1].content)
    rewritten_query = rewrite_data.get("rewritten_query") or state["query"]

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