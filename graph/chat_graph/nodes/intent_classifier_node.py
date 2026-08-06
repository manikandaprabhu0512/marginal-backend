import json

from agents.intent_router_agent import get_intent_router_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def intent_classifier_node(state: ChatState):
    intent_router_agent = get_intent_router_agent()

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.UNDERSTANDING_INTENT,
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
        lambda: intent_router_agent.ainvoke({"messages": [{"role": "user", "content": input_payload}]})
    )

    data = parse_agent_json(result["messages"][-1].content)
    
    return {
        "query_intent": data["intent_type"],
        "answer": data["direct_answer"]
    }