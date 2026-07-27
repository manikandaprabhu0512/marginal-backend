import os

from langchain_mcp_adapters.client import MultiServerMCPClient

_client = None
_tools_cache = None

async def get_all_mcp_tools():
    global _client, _tools_cache
    if _tools_cache is not None:
        return _tools_cache
    
    print("Getting Tools Ready...")

    _client = MultiServerMCPClient(
        {
            "bright_data": {
                "url": f"https://mcp.brightdata.com/sse?token={os.getenv('BRIGHTDATA_API_TOKEN')}",
                "transport": "sse",
            }
        }
    )
    _tools_cache = await _client.get_tools()
    return _tools_cache