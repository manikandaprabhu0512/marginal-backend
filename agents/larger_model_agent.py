from langchain.agents import create_agent
from models.model import larger_model
from prompts import load_prompt

_larger_model_agent = None

async def get_larger_model_agent(conversation_id: str):
    global _larger_model_agent
    if _larger_model_agent is None:
        _larger_model_agent = create_agent(
            model=larger_model,
            tools = [],
            system_prompt=load_prompt("large_model_agent_prompt"),
            name="larger_answer_agent"
        )
    
    return _larger_model_agent