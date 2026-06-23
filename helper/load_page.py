from helper.web_loader import web_loader_tool


async def load_page(page: dict) -> dict:
    """Load a single page's content — called in parallel for all pages."""
    try:
        content = await web_loader_tool(page["url"])
        if content.startswith("ERROR:"):
            return None
        return {**page, "raw_content": content}
    except Exception as e:
        print(f"Failed to load {page['url']}: {e}")
        return None