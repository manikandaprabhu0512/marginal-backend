from langchain.agents import create_agent
from models.model import larger_model
from prompts import load_prompt

_confidence_agent = create_agent(
        larger_model,
        [],
        system_prompt=load_prompt("confidence_agent_prompt"),
        name="confidence_agent"
    )


def get_confidence_agent():
    return _confidence_agent