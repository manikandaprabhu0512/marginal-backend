import os

from langchain_mcp_adapters.client import MultiServerMCPClient

_client = None
_tools_cache = None

async def get_all_mcp_tools():
    global _client, _tools_cache
    if _tools_cache is not None:
        return _tools_cache

    _client = MultiServerMCPClient(
        {
            "Bright Data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": {
                    "API_TOKEN": os.getenv("BRIGHTDATA_API_TOKEN"),
                    "GROUPS": "advanced_scraping"
                },
                "transport": "stdio",
            },
        }
    )
    _tools_cache = await _client.get_tools()
    return _tools_cache