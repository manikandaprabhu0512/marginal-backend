import json

from agents.larger_model_agent import get_larger_model_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def larger_model_node(state: ChatState):

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.LARGER_MODEL_GENERATING_ANSWER,
            data={},
        )
    )

    larger_agent = await get_larger_model_agent(state["conversation_id"])

    input_payload = json.dumps(
        {
            "query": state["message"],
            "context": state["context"],
            "history": state["history"],
            "excluded_urls": state["excluded_urls"],
        }
    )

    result = await retry_async(
        lambda: larger_agent.ainvoke({"messages": [{"role": "user","content": input_payload}]})
    )

    data = parse_agent_json(result["messages"][-1].content)

    return {
        "answer": data["answer"],
        "source": data["source"],
        "model_used": "larger_model",
    }