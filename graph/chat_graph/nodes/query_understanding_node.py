import json

from agents.query_understanding_agent import get_query_understanding_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def query_understanding_node(state: ChatState):
    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.UNDERSTANDING_QUERY,
            data={},
        )
    )

    understanding_agent = get_query_understanding_agent()

    query_payload = json.dumps({"query": state["message"], "history": state["history"]})

    result = await retry_async(
        lambda: understanding_agent.ainvoke(
            {"messages": [{"role": "user", "content": query_payload}]}
        )
    )

    data = parse_agent_json(result["messages"][-1].content)

    return {
        "query_type": data["type"],
        "rewritten_query": data["rewritten_query"],
        "answer": data["direct_answer"]
    }