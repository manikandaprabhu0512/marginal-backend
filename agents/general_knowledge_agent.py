from langchain.agents import create_agent

from models.model import groq_model
from prompts import load_prompt

_general_knowledge_agent = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("general_knowledge_agent_prompt"),
    name="general_knowledge_agent"
)

def get_general_knowledge_agent():
    return _general_knowledge_agent