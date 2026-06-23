from langchain.agents import create_agent
from models.model import smaller_model
from prompts import load_prompt

_smaller_model_agent = None

async def get_smaller_model_agent(conversation_id: str):
    global _smaller_model_agent
    if _smaller_model_agent is None:
        _smaller_model_agent = create_agent(
            smaller_model,
            [],
            system_prompt=load_prompt("smaller_model_agent_prompt"),
            name="smaller_model_agent"
        )

    return _smaller_model_agent