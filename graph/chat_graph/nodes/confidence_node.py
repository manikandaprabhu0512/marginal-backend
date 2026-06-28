import json

from agents.confidence_agent import get_confidence_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def confidence_node(state: ChatState):

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.CHECKING_CONFIDENCE,
            data={},
        )
    )

    confidence_agent = get_confidence_agent()

    input_payload = json.dumps(
        {
            "query": state["message"],
            "context": state["context"],
            "answer": state["answer"],
            "source": state["source"],
        }
    )

    result = await retry_async(
        lambda: confidence_agent.ainvoke({"messages": [{"role": "user","content": input_payload}]})
    )

    confidence = parse_agent_json(result["messages"][-1].content)["confidence"]

    return {"confidence": confidence}