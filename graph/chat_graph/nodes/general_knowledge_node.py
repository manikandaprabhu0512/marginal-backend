import json

from agents.general_knowledge_agent import get_general_knowledge_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def general_knowledge_node(state: ChatState):
    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.GENERATING_ANSWER,
            data={},
        )
    )

    general_knowledge_agent = get_general_knowledge_agent()

    general_knowledge_payload = json.dumps({"query": state["rewritten_query"]})

    result = await retry_async(
        lambda: general_knowledge_agent.ainvoke({"messages": [{"role": "user", "content": general_knowledge_payload}]})
    )

    data = parse_agent_json(result["messages"][-1].content)
    print(data)

    return {"answer": data["answer"], "source": "general_knowledge"}