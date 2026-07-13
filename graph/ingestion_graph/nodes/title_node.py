import json

from agents.title_agent import get_title_agent
from db.crud import db_get_conversation, update_conversation_title
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.json_parser import parse_agent_json
from helper.retry import retry_async
from telemetry.instrumentation import tracer

async def title_node(state: GraphState):
    with tracer.start_as_current_span("Title"):
        conversation = await db_get_conversation(state["conversation_id"])

        if conversation.title != "Untitled Notebook":
            return {}

        title_agent = get_title_agent()

        with tracer.start_as_current_span("Generating title"):
            result = await retry_async(
                lambda: title_agent.ainvoke(
                    {"messages": [{"role": "user", "content": json.dumps({"query": state["rewritten_query"]})}]}
                )
            )

        with tracer.start_as_current_span("Parsing title"):
            title_data = parse_agent_json(result["messages"][-1].content)

        title = title_data.get("title","Untitled Notebook")

        with tracer.start_as_current_span("Saving title"):
            await retry_async(
                lambda: update_conversation_title(state["conversation_id"],title)
            )

        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=IngestionEventType.TITLE_GENERATED,
                data={
                    "title": title,
                },
            )
        )

        return {}