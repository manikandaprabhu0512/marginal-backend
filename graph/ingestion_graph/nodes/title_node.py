import json

from agents.title_agent import get_title_agent
from db.crud import db_get_conversation, update_conversation_title
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def title_node(state: GraphState):
    print("Title Node Called...")

    conversation = await db_get_conversation(state["conversation_id"])

    print("Recieved Conversation...")

    if conversation.title != "Untitled Notebook":
        return {}

    title_agent = get_title_agent()

    print("Got Title Agent...")

    result = await retry_async(
        lambda: title_agent.ainvoke(
            {"messages": [{"role": "user", "content": json.dumps({"query": state["rewritten_query"]})}]}
        )
    )

    print("Result Generated...")

    title_data = parse_agent_json(result["messages"][-1].content)

    title = title_data.get("title","Untitled Notebook")

    print("Title: ", title)

    await retry_async(
        lambda: update_conversation_title(state["conversation_id"],title)
    )

    print("Title Updated...")

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=IngestionEventType.TITLE_GENERATED,
            data={
                "title": title,
            },
        )
    )

    print("Event Published...")

    return {}