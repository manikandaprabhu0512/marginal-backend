import json
from urllib.parse import urlparse

from mcp_setup.tool_registry import get_tool_by_name


async def search_urls(query: str) -> list[dict]:
    search_tool = await get_tool_by_name("search_engine")
    result = await search_tool.ainvoke({"query": query})

    raw_text = result[0]["text"]
    data = json.loads(raw_text)
    organic = data.get("organic", [])

    SKIP_DOMAINS = [
        "youtube.com", "youtu.be", "twitter.com", "x.com",
        "instagram.com", "facebook.com", "linkedin.com",
        "reddit.com", "pinterest.com", "tiktok.com"
    ]

    PREFERRED_DOMAINS = [
        "wikipedia.org", "github.com", ".gov", ".edu",
        "docs.", "developer."
    ]
    
    seen_domains = set()
    preferred = []
    others = []

    for r in organic:
        url = r["link"]
        domain = urlparse(url).netloc

        if any(skip in domain for skip in SKIP_DOMAINS):
            continue

        if domain in seen_domains:
            continue
        seen_domains.add(domain)

        item = {"title": r.get("title", url), "url": url}

        if any(pref in domain for pref in PREFERRED_DOMAINS):
            preferred.append(item)
        else:
            others.append(item)

    return (preferred + others)[:10]