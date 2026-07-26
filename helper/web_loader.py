import traceback

from config.crawl4ai_config import crawler


async def web_loader_tool(url: str):
    try:
        
        result = await crawler.arun(url)

        if not result.success:
            print(result.error_message)
            return

        return result.markdown

    except Exception:
        traceback.print_exc()
        raise