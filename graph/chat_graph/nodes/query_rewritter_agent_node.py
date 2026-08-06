import json

from agents.query_rewritter_agent import get_query_rewritter_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def query_rewritter_node(state: ChatState):
    query_rewritter_agent = get_query_rewritter_agent()

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.QUERY_REWRITTER,
            data={},
        )
    )

    input_payload = json.dumps(
        {
            "query": state["message"],
            "previous_message": state["history"]
        }
    )

    result = await retry_async(
        lambda: query_rewritter_agent.ainvoke({"messages": [{"role": "user", "content": input_payload}]})
    )

    data = parse_agent_json(result["messages"][-1].content)

    return {
        "rewritten_query": data["rewritten_query"]
    }