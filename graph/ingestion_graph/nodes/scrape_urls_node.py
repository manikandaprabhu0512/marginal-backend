from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.retry import retry_async
from telemetry.instrumentation import tracer
from tools.content_scraper_tool import search_urls


async def search_node(state: GraphState):
    with tracer.start_as_current_span("Scraping URLs"):

        with tracer.start_as_current_span("Scraping"):
            scraped_urls = await retry_async(
                lambda: search_urls(state["rewritten_query"])
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
            "url_list": scraped_urls,
        }