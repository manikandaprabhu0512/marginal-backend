from mcp_setup.mcp_client import get_all_mcp_tools


async def get_tool_by_name(name: str):
    tools = await get_all_mcp_tools()
    matches = [t for t in tools if t.name == name]
    if not matches:
        available = [t.name for t in tools]
        raise ValueError(f"Tool '{name}' not found. Available: {available}")
    return matches[0]

async def get_tools_by_names(names: list[str]):
    tools = await get_all_mcp_tools()
    return [t for t in tools if t.name in names]