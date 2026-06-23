from langchain.agents import create_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from models.model import smaller_model
from prompts.__init__ import load_prompt

search = GoogleSerperAPIWrapper()

_content_scraper_agent = None

async def get_content_scraper_agent():
    global _content_scraper_agent
    if _content_scraper_agent is None:
        _content_scraper_agent = create_agent(
            model=smaller_model,
            tools=[search.run],
            system_prompt=load_prompt("content_scraper_agent_prompt"),
            name="content_scraper_agent"
        )
    return _content_scraper_agent