from db.crud import add_scrapedURL
from db.models import ScrapedURLs
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.retry import retry_async
from tools.content_scraper_tool import search_urls


async def search_node(state: GraphState):
    scraped_urls = await ScrapedURLs.find_one(
        ScrapedURLs.conversation_id == state["conversation_id"],
        ScrapedURLs.query == state["rewritten_query"]
    )

    if scraped_urls:
        return {
            "url_list": scraped_urls.url_list
        }

    scraped_urls = await retry_async(
        lambda: search_urls(state["rewritten_query"])
    )

    await retry_async(
        lambda: add_scrapedURL(state["conversation_id"],state["rewritten_query"],scraped_urls)
    )

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=IngestionEventType.SEARCH_COMPLETED,
            data={
                "urls_found": len(scraped_urls),
            },
        )
    )

    return {
        "url_list": scraped_urls
    }