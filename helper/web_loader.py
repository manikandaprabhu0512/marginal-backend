import re

import httpx
from bs4 import BeautifulSoup

from config.crawl4ai_config import crawler, run_config


async def web_loader_tool(link: str):
    """Fetch and extract clean text content from a given URL."""
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get(link)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
        clean_text = re.sub(r'\s+', ' ', text).strip()
        return clean_text

    except Exception as e:
        try:
            print(f"BeautifulSoup failed for {link}. Falling back to Crawl4AI...")

            result = await crawler.arun(link, config=run_config)

            return result.markdown

        except Exception as e:
            return f"ERROR: failed to load {link} - {str(e)}"