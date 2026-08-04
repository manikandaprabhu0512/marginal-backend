from langchain.agents import create_agent

from models.model import groq_model
from prompts import load_prompt

_filler_agent = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("filler_agent_prompt"),
    name="filler_agent"
)

def get_filler_agent():
    return _filler_agent