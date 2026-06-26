import json

from agents.title_agent import get_title_agent
from db.crud import get_or_create_conversation, update_conversation_title
from graph.state import GraphState
from helper.event_bus import Event, EventType, event_bus
from helper.json_parser import parse_agent_json


async def title_node(state: GraphState):
    conversation = await get_or_create_conversation(state["conversation_id"])

    if conversation is None:
        raise ValueError("Conversation not found.")

    # Already completed
    if conversation.title != "Untitled Notebook":
        return {}


    title_agent = get_title_agent()
    title_result = await title_agent.ainvoke(
        {"messages": [{"role": "user", "content": json.dumps({"query": state["query"]})}]}
    )
    title_data = parse_agent_json(title_result["messages"][-1].content)
    title = title_data.get("title", "Untitled Notebook")
    await update_conversation_title(state["conversation_id"], title)

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=EventType.TITLE_GENERATED,
            data={
                "title": title
            }
        )
    )

    return {}