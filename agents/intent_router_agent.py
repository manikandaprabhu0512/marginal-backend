from langchain.agents import create_agent

from models.model import groq_model
from prompts import load_prompt

_intent_router_agent = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("intent_router_agent_prompt"),
    name="intent_router_agent"
)

def get_intent_router_agent():
    return _intent_router_agent