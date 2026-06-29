from langchain.agents import create_agent

from models.model import groq_model
from prompts import load_prompt

_query_understanding_agent = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("query_understanding_agent_prompt"),
    name="query_understanding_agent"
)

def get_query_understanding_agent():
    return _query_understanding_agent