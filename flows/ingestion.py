import asyncio
import json

from agents.title_agent import get_title_agent
from db.crud import save_sources, update_conversation_title
from flows.chat_flow import run_chat
from helper.file_type import detect_source_type
from helper.json_parser import parse_agent_json
from helper.load_page import load_page
from helper.process_page import process_page
from helper.sse_event import sse_event
from tools.content_scraper_tool import search_urls


async def run_ingestion_stream(conversation_id: str, query: str):

    # Stage 1: title 
    title_agent = get_title_agent()
    title_result = await title_agent.ainvoke(
        {"messages": [{"role": "user", "content": json.dumps({"query": query})}]}
    )
    title_data = parse_agent_json(title_result["messages"][-1].content)
    title = title_data.get("title", "Untitled Notebook")
    await update_conversation_title(conversation_id, title)
    yield sse_event("title_generated", {"title": title})
    print("Title updated...\n")

    # content_scraper_agent = await get_content_scraper_agent()
    # scraper_result = await content_scraper_agent.ainvoke(
    #     {"messages": [{"role": "user", "content": query}]}
    # )
    # scraper_data = parse_agent_json(scraper_result["messages"][-1].content)
    # url_list = scraper_data.get("pages", [])
    # yield sse_event("scraping_complete", {"urls_found": len(url_list)})
    # print("URL Scraped...\n")

    # Stage 2: content scraper
    url_list = await search_urls(query)
    yield sse_event("scraping_complete", {"urls_found": len(url_list)})

    # Stage 3: page loader
    loaded_pages = await asyncio.gather(
        *[load_page(page) for page in url_list],
        return_exceptions=False
    )
    pages = [p for p in loaded_pages if p is not None]
    yield sse_event("pages_loaded", {"pages_loaded": len(pages)})
    print("Pages loaded...\n")

    # Stage 4: page vectorizer
    page_results = await asyncio.gather(
        *[process_page(page, conversation_id) for page in pages],
        return_exceptions=True
    )
    yield sse_event("pages_vectorized", {})
    print("Pages Vectorized...\n")

    # Stage 5: save sources
    sources = []
    for r in page_results:
        if isinstance(r, Exception):
            print(f"Page processing failed: {r}")
            continue
        if r["title"] and r["url"]:
            sources.append({
                "title": r["title"],
                "url": r["url"],
                "source_type": detect_source_type(r["url"]),
                "vector_ids": r.get("vector_ids") or []
            })
            
    await save_sources(conversation_id, sources)
    yield sse_event("ingestion_complete", {
        "urls_found": len(url_list),
        "urls_stored": len(sources),
        "sources": sources
    })
    print("Sources saved...\n")

    # Stage 6: chat
    async for item in run_chat(conversation_id, query, [], False):
        yield item
