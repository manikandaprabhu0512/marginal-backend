from langchain.agents import create_agent

from mcp_setup.tool_registry import get_tool_by_name
from models.model import groq_model
from prompts.__init__ import load_prompt

_content_scraper_agent = None

async def get_content_scraper_agent():
    global _content_scraper_agent
    if _content_scraper_agent is None:
        search_tool = await get_tool_by_name("search_engine")
        _content_scraper_agent = create_agent(
            model=groq_model,
            tools=[search_tool],
            system_prompt=load_prompt("content_scraper_agent_prompt"),
            name="content_scraper_agent"
        )
    return _content_scraper_agent