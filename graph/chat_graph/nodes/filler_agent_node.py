import json

from agents.filler_agent import get_filler_agent
from graph.chat_graph.chat_state import ChatState
from helper.json_parser import parse_agent_json
from helper.retry import retry_async


async def filler_agent_node(state: ChatState):
    
    input_payload = json.dumps(
        {
            "query": state["message"],
        }
    )

    filler_agent = get_filler_agent()

    result = await retry_async(
        lambda: filler_agent.ainvoke(
            {"messages": [{"role": "user","content": input_payload}]}
        )
    )

    data = parse_agent_json(result["messages"][-1].content)

    return {
        "answer": data["response"],
        "is_filler": data["is_filler"],
    }