from db.crud import add_scrapedURL
from db.models import ScrapedURLs
from graph.state import GraphState
from helper.event_bus import Event, EventType, event_bus
from tools.content_scraper_tool import search_urls


async def search_node(state: GraphState):
    scraped_urls = await ScrapedURLs.find_one(
        ScrapedURLs.conversation_id == state["conversation_id"],
        ScrapedURLs.query == state["query"]
    )

    if scraped_urls:
        return {
            "url_list": scraped_urls.url_list
        }

    scraped_urls = await search_urls(state["query"])

    await add_scrapedURL(state["conversation_id"], state["query"], scraped_urls)

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=EventType.SEARCH_COMPLETED,
            data={
                "urls_found": len(scraped_urls),
            },
        )
    )

    return {
        "url_list": scraped_urls
    }