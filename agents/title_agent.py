from langchain.agents import create_agent
from models.model import groq_model
from prompts import load_prompt

_title_agent = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("title_agent_prompt"),
    name="title_agent"
)

def get_title_agent():
    return _title_agent