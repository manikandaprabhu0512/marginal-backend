# agents/sources_summary_agent.py
from langchain.agents import create_agent

from models.model import groq_model
from prompts import load_prompt

_sources_summary_agent = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("source_summary_agent_prompt"),
    name="sources_summary_agent"
)

def get_sources_summary_agent():
    return _sources_summary_agent