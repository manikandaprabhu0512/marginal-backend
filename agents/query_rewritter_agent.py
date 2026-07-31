# agents/sources_summary_agent.py
from langchain.agents import create_agent

from models.model import groq_model
from prompts import load_prompt

_query_rewritter_agent = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("query_rewritter_agent_prompt"),
    name="query_rewritter_agent"
)

def get_query_rewritter_agent():
    return _query_rewritter_agent